class Client extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            currentUser: {},
            mode: "Lobby"
        }
    }

    render() {
        if(this.state.mode === "Lobby") {
            return <Lobby currentUser={this.state.currentUser}/>
        }
    }
}

class Lobby extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            games: [],
            chatEvents: [],
            users: []
        };
    }

    render() {
        return (
            <div className="lobby-layout">
                <div className="left">
                    <CurrentGames games={this.state.games}/>
                </div>
                <div className="center">
                    <LobbyChat events={this.state.chatEvents}
                               currentUser={this.props.currentUser}/>
                </div>
                <div className="right">
                    <ConnectedUsersList users={this.state.users}/>
                </div>
            </div>
        )
    }

    componentDidMount() {
        ws.send_async_callbacks["lobby_chatevent"] = ((message) => {
            this.setState((props, state) => {
                if(state.chatEvents === undefined) return;
                state.chatEvents.push(message)
            })
        });
    }

    componentWillUnmount() {
        delete ws.send_async_callbacks["lobby_chatevent"]
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
    render() {
        //Create lobbychatmessages from this.props.messages
        let events = [];
        for(let i = 0; i < this.props.events.length; i++) {
            let event = this.props.events[i];
            //TODO: add other events
            if(event.event === "UserSentMessageEvent") {
                let node = <LobbyChatMessage sender={event.user}
                                             content={event.message}
                                             timestamp={event.timestamp}
                                             key={event.guid}/>;
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
                    <LobbyChatMessageBox currentUser={this.props.currentUser} disabled={false}/>
                </div>
            </div>
        )
    }
}

class LobbyChatMessage extends React.Component {
    render() {
        return (
            <div className="message">
                <div className="sender">
                    <UserName user={this.props.sender}/>
                </div>
                <div className="content">
                    {this.props.content}
                </div>
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

    sendMessage = (e) => {
        ws.call_client_command("lobby.sendmsg", {
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
                <div className="lower-box">
                    <ul>
                        {users}
                    </ul>
                </div>
            </div>
        )
    }
}

class UserName extends React.Component {
    render() {
        return <span>{this.props.user.name}</span>;
    }
}

function updateUI() {
    ReactDOM.render(<Client/>, document.getElementById("react-app"));
}

console.log("Trying to connect to ws://lo.steffo.eu:1234...");
let ws = new WebSocket("ws://lo.steffo.eu:1234");
ws.send_async = function(data, callback) {
    ws.send_async_callbacks[ws.send_async_count] = callback;
    data["id"] = ws.send_async_count;
    ws.send_async_count++;
    ws.send(JSON.stringify(data));
};
ws.call_client_command = function(command, data, callback) {
    ws.send_async({
        "command": command,
        "data": data
    }, callback)
};
ws.onopen = function() {
    ws.send_async_callbacks = {};
    ws.send_async_count = 0;
    updateUI();
};
ws.onmessage = function(message) {
    let data = JSON.parse(message.data);
    if(data.success === false)
    {
        console.error("Failure in the message:");
        console.error(data);
        return;
    }
    let id = data["id"];
    if(id === undefined) {
        console.error("No id supplied in the message:");
        console.error(data);
        return;
    }
    if(data.hasOwnProperty(id))
    {
        console.log("Ignored message because of no id:");
        console.log(data);
        return;
    }
    let func = ws.send_async_callbacks[id];
    if(func === undefined)
    {
        console.log("Ignored message because of no associated callback:");
        console.log(data);
        return;
    }
    func(message);
    delete ws.send_async_callbacks[id];
};
ws.onclose = function() {
    ReactDOM.render(
    <div>Server connection lost :(</div>,
    document.getElementById("react-app"));
};