class Client extends React.Component {
    render() {
        if(this.props.data.mode === "Lobby") {
            return <Lobby games={this.props.data.lobby.games}
                          events={this.props.data.lobby.events}
                          users={this.props.data.lobby.users}
                          currentUser={this.props.data.current_user}/>
        }
    }
}

class Lobby extends React.Component {
    render() {
        return (
            <div className="lobby-layout">
                <div className="left">
                    <CurrentGames games={this.props.games}/>
                </div>
                <div className="center">
                    <LobbyChat events={this.props.events}
                               currentUser={this.props.currentUser}/>
                </div>
                <div className="right">
                    <ConnectedUsersList users={this.props.users}/>
                </div>
            </div>
        )
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
                    <Button disabled={false} label="Create game" /*onClick={}*//>
                </div>
            </div>
        )
    }

    refresh = function() {
        ws.send(JSON.stringify({
            "command": "lobby.get_games_list"
        }))
    }

    componentDidMount() {
        this.refresh();
        this.refresher = setInterval(this.refresh, 2000)
    }

    componentWillUnmount() {
        clearInterval(this.refresher)
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

    refresh = function() {
        ws.send(JSON.stringify({
            "command": "lobby.get_unread_messages"
        }))
    };

    componentDidMount() {
        this.refresh();
        this.refresher = setInterval(this.refresh, 2000)
    }

    componentWillUnmount() {
        clearInterval(this.refresher)
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
    render() {
        return (
            <div className="message-box">
                <div className="sender">
                    <UserName user={this.props.currentUser}/>
                </div>
                <div className="input">
                    <TextInput disabled={this.props.disabled} placeholder="Send messages here!" /*onChange={}*//>
                </div>
                <div className="send">
                    <Button disabled={this.props.disabled} label="Send"/>
                </div>
            </div>
        )
    }
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

    refresh = function() {
        ws.send(JSON.stringify({
            "command": "lobby.get_users_list"
        }))
    };

    componentDidMount() {
        this.refresh();
        this.refresher = setInterval(this.refresh, 2000)
    }

    componentWillUnmount() {
        clearInterval(this.refresher)
    }
}

class UserName extends React.Component {
    render() {
        return <span>{this.props.user.name}</span>;
    }
}

let game_data = {
    mode: "Lobby",
    current_user: {
        name: undefined,
        guid: undefined
    },
    lobby: {
        games: [],
        events: [],
        users: [],
    }
};

function updateUI() {
    ReactDOM.render(<Client data={game_data}/>, document.getElementById("react-app"));
}

function getSelf() {
    ws.send(JSON.stringify({
        "command": "lobby.get_self"
    }))
}

console.log("Trying to connect to ws://lo.steffo.eu:1234...");
const ws = new WebSocket("ws://lo.steffo.eu:1234");
ws.onopen = function() {
    getSelf();
};
ws.onmessage = function(message) {
    let data = JSON.parse(message.data);
    if(data.success === false)
    {
        console.error(`Error in request ${data.request}.`);
        return;
    }
    if(data.request === "lobby.get_self")
    {
        game_data.current_user = data.data;
    }
    else if(data.request === "lobby.get_games_list")
    {
        game_data.lobby.games = data.data;
    }
    else if(data.request === "lobby.get_unread_messages")
    {
        for(let i = 0; i < data.data.length; i++)
        {
            let event = data.data[i];
            game_data.lobby.events.push(event);
        }
    }
    else if(data.request === "lobby.get_users_list")
    {
        game_data.lobby.users = data.data;
    }
    updateUI();
};
ws.onclose = function() {
    ReactDOM.render(
    <div>Server connection lost :(</div>,
    document.getElementById("react-app"));
};