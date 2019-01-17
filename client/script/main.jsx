'use strict';

class Client extends React.Component {
    ws;

    constructor(props) {
        super(props);
        this.state = {
            mode: "Lobby",
            data: {
                currentUser: {},
                games: [],
                users: []
            }
        };

        this.ws = new WebSocket(prompt("Connect to?", "ws://lo.steffo.eu:1234"));

        //Define custom websocket functions
        {
            this.ws.send_async_callbacks = {};
            this.ws.send_async_count = 0;

            this.ws.register_callback = (name, callback, caller) => {
                if(caller !== undefined) {
                    callback.bind(caller);
                }
                this.ws.send_async_callbacks[name] = callback;
            };

            this.ws.unregister_callback = (name) => {
                this.ws.send_async_callbacks[name] = undefined;
            };

            this.ws.send_async = (data, callback) => {
                this.ws.register_callback(data["id"], callback, this);
                data["id"] = String(this.ws.send_async_count);
                this.ws.send_async_count++;
                this.ws.send(JSON.stringify(data));
            };

            this.ws.call_client_command = (command, data, callback) => {
                this.ws.send_async({
                    "command": command,
                    "data": data
                }, callback)
            };
        }

        //Define standard websocket functions
        {
            this.ws.onopen = () => {
                this.ws.call_client_command("lobby.info", {}, (data) => {
                    this.setState({
                        data: {
                            currentUser: data.currentUser,
                            games: data.games,
                            users: data.users
                        }
                    });
                });
            };

            this.ws.onmessage = (message) => {
                let data = JSON.parse(message.data);
                if(data.success === false)
                {
                    console.error("Failure in the message:");
                    console.error(data);
                    return;
                }
                let id = String(data["id"]);
                if(id === undefined) {
                    console.error("No id supplied in the message:");
                    console.error(data);
                    return;
                }
                let func = this.ws.send_async_callbacks[id];
                if(func === undefined)
                {
                    return;
                }
                func(data);
                if(!isNaN(id))
                {
                    this.ws.unregister_callback(id);
                }
            };

            this.ws.onclose = () => {
            };
        }
    }

    render() {
        if(this.state.mode === "Lobby") {
            return <Lobby clientData={this.state.data}
                          ws={this.ws}/>
        }
        return <div>Nothing to render.</div>
    }

    componentWillUnmount() {
        this.ws.close(1001, "Client component is unmounting");
    }
}

class Lobby extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            chatEvents: []
        }
    }

    render() {
        return (
            <div className="lobby-layout">
                <div className="left">
                    <CurrentGames games={this.props.clientData.games}/>
                </div>
                <div className="center">
                    <LobbyChat events={this.state.chatEvents}
                               currentUser={this.props.clientData.currentUser}
                               ws={this.props.ws}/>
                </div>
                <div className="right">
                    <ConnectedUsersList users={this.props.clientData.users}/>
                </div>
            </div>
        )
    }

    componentDidMount() {
        this.props.ws.send_async_callbacks["lobby_chatevent"] = ((event) => {
            this.setState(function(state) {
                let chatEvents = state.chatEvents;
                chatEvents.push(event.event);
                return {chatEvents: chatEvents};
            });
        });
    }

    componentWillUnmount() {
        delete this.props.ws.send_async_callbacks["lobby_chatevent"]
    }
}

class CurrentGames extends React.Component {
    render() {
        //Create game listings from this.props.games
        let game_listings = [];
        for(let i = 0; i < this.props.games.length; i++) {
            let game = this.props.games[i];
            let game_listing = (
                <GameListing name={game.name}
                             status={game.status}
                             players={game.players}
                             maxPlayers={game.maxPlayers}
                             key={game.guid}/>
            );
            game_listings.push(game_listing);
        }
        return (
            <div className="box game-listing-box">
                <div className="upper-box">
                    Current games
                </div>
                <div className="middle-box">
                    {game_listings}
                </div>
                <div className="lower-box">
                    <Button disabled={true} label="Create game" /*onClick={}*//>
                </div>
            </div>
        )
    }
}

class GameListing extends React.Component {
    render() {
        let status = "???";
        let button = {
            label: "???",
            disabled: true
        };
        if(this.props.status === "joinable")
        {
            status = `${this.props.players}/${this.props.maxPlayers}`;
            button.label = "Join";
            button.disabled = false;
        }
        else if(this.props.status === "in-progress")
        {
            status = `In progress`;
            button.label = "";
        }
        else if(this.props.status === "joined")
        {
            status = `${this.props.players}/${this.props.maxPlayers}`;
            button.label = "Leave";
            button.disabled = false;
        }
        return (
            <div className={`game-listing ${this.props.status}`}>
                <div className="name">{this.props.name}</div>
                <div className="status">{status}</div>
                <div className="join">
                    <Button
                        label={button.label}
                        disabled={button.disabled}
                        /*onClick={}*//>
                </div>
            </div>
        )
    }
}

class Button extends React.Component {
    render() {
        if(this.props.disabled === true)
        {
            return <button disabled={true}>{this.props.label}</button>
        }
        else
        {
            return <button onClick={this.props.onClick}>{this.props.label}</button>
        }
    }
}

class LobbyChat extends React.Component {
    constructor(props) {
        super(props);
        this.lastMessageRef = React.createRef();
    }

    render() {
        //Create lobbychatmessages from this.props.messages
        let events = [];
        for(let i = 0; i < this.props.events.length; i++) {
            let event = this.props.events[i];
            let ref = undefined;
            if(i + 1 === this.props.events.length) ref = this.lastMessageRef;
            if(event.event_name === "UserSentMessageEvent") {
                let node = <LobbyChatMessage sender={event.user}
                                             message={event.message}
                                             timestamp={event.timestamp}
                                             key={event.guid}
                                             superRef={ref}/>;
                events.push(node);
            }
            else if(event.event_name === "UserJoinedEvent") {
                let node = <LobbyChatUserJoinedMessage user={event.user}
                                                       key={event.guid}
                                                       superRef={ref}/>;
                events.push(node);
            }
            else if(event.event_name === "UserLeftEvent") {
                let node = <LobbyChatUserLeftMessage user={event.user}
                                                     key={event.guid}
                                                     superRef={ref}/>;
                events.push(node);
            }
        }
        return (
            <div className="box chat-box">
                <div className="upper-box">
                    Lobby chat
                </div>
                <div className="middle-box">
                    {events}
                </div>
                <div className="lower-box">
                    <LobbyChatMessageBox currentUser={this.props.currentUser} disabled={false} ws={this.props.ws}/>
                </div>
            </div>
        )
    }

    componentDidUpdate() {
        this.lastMessageRef.current.scrollIntoView();
    }
}

class LobbyChatMessage extends React.Component {
    render() {
        return (
            <div ref={this.props.superRef} className="message">
                <div className="sender">
                    <UserName user={this.props.sender}/>
                </div>
                <div className="content">
                    {this.props.message}
                </div>
            </div>
        )
    }
}

class LobbyChatUserJoinedMessage extends React.Component {
    render() {
        return (
            <div ref={this.props.superRef} className="service-message user-joined">
                <span>{this.props.user.name}</span> joined the lobby.
            </div>
        )
    }
}

class LobbyChatUserLeftMessage extends React.Component {
    render() {
        return (
            <div ref={this.props.superRef} className="service-message left">
                <span>{this.props.user.name}</span> left the lobby.
            </div>
        )
    }
}

class LobbyChatMessageBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            "currentMessage": ""
        }
    }

    render() {
        if(this.props.disabled) {
            return (
                <div className="message-box">
                    <div className="sender">
                        <UserName user={this.props.currentUser}/>
                    </div>
                    <div className="input">
                        <TextInput disabled={true} placeholder="Chat disabled"/>
                    </div>
                    <div className="send">
                        <Button disabled={true} label="Send"/>
                    </div>
                </div>
            )
        }
        else {
            return (
                <div className="message-box">
                    <div className="sender">
                        <UserName user={this.props.currentUser}/>
                    </div>
                    <div className="input">
                        <TextInput disabled={false}
                                   placeholder="Send messages here!"
                                   onChange={this.onTextInput}
                                   onKeyPress={this.onKeyPress}
                                   value={this.state.currentMessage}/>
                    </div>
                    <div className="send">
                        <Button disabled={false} label="Send" onClick={this.sendMessage}/>
                    </div>
                </div>
            )
        }
    }

    onTextInput = (e) => {
        this.setState({currentMessage: e.target.value});
    };

    onKeyPress = (e) => {
        if(e.key === "Enter") {
            this.sendMessage(e);
        }
    };

    sendMessage = (e) => {
        if(this.state.currentMessage === "") return;

        this.props.ws.call_client_command("lobby.sendmsg", {
            "text": this.state.currentMessage
        }, () => {});

        this.setState({currentMessage: ""});
    };
}

class TextInput extends React.Component {
    render() {
        if(this.props.disabled === true) {
            return (
                 <input type="text"
                        placeholder={this.props.placeholder}
                        disabled={true}
                 />
            )
        }
        else {
            return (
                 <input type="text"
                        placeholder={this.props.placeholder}
                        onChange={this.props.onChange}
                        onKeyPress={this.props.onKeyPress}
                        value={this.props.value}
                 />
            )
        }
    }
}

class ConnectedUsersList extends React.Component {
    render() {
        let users = [];
        for(let i = 0; i < this.props.users.length; i++) {
            let user = this.props.users[i];
            console.log(user);
            let node = (
                <li key={user.guid}>
                    <UserName user={user}/>
                </li>);
            users.push(node);
        }
        return (
            <div className="box connected-users-box">
                <div className="upper-box">
                    Connected
                </div>
                <div className="middle-box">
                    <ul>
                        {users}
                    </ul>
                </div>
                <div className="lower-box">
                </div>
            </div>
        )
    }
}

class UserName extends React.Component {
    render() {
        let name;
        if(this.props.user === undefined) {
            name = "..."
        }
        else {
            name = this.props.user.name;
        }
        return <span>{name}</span>;
    }
}

ReactDOM.render(<Client/>, document.getElementById("react-app"));