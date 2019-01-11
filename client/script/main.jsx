class Client extends React.Component {
    render() {
        if(this.props.mode === "Lobby") {
            return <Lobby>Client</Lobby>
        }
    }
}

class Lobby extends React.Component {
    render() {
        return (
            <div className="lobby-layout">
                <div className="left">
                    <CurrentGames/>
                </div>
                <div className="center">
                    <LobbyChat/>
                </div>
                <div className="right">
                    <ConnectedUsersList/>
                </div>
            </div>
        )
    }
}

class CurrentGames extends React.Component {
    render() {
        return (
            <div className="box game-listing-box">
                <div className="upper-box">
                    Current games
                </div>
                <div className="middle-box">
                    <GameListing
                        gameId={1}
                        name="Town of Salem"
                        status="joinable"
                        players={6}
                        maxPlayers={16}>
                    </GameListing>
                    <GameListing
                        gameId={2}
                        name="Thatguy's game"
                        status="in-progress">
                    </GameListing>
                    <GameListing
                        gameId={3}
                        name="Mifia 15"
                        status="joined"
                        players={11}
                        maxPlayers={16}>
                    </GameListing>
                </div>
                <div className="lower-box">
                    <Button disabled={false} label="Create game" /*onClick={}*//>
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
            <div className={`game-listing ${this.props.status}`} id={`game-listing-${this.props.gameId}`}>
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
        return (
            <div className="box chat-box">
                <div className="upper-box">
                    Lobby chat
                </div>
                <div className="middle-box">
                    <LobbyChatMessage sender={{name: "Steffo"}} content="Qualcuno fa una partita?"/>
                    <LobbyChatMessage sender={{name: "Ciao123"}} content="Io, volentieri."/>
                    <LobbyChatMessage sender={{name: "Edgyboi"}} content="Io no. Ho cose molto più importanti da fare."/>
                </div>
                <div className="lower-box">
                    <LobbyChatMessageBox sender={{name: "Steffo"}} disabled={false}/>
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
                    {this.props.sender.name}
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
                    {this.props.sender.name}
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
        return (
            <div className="box connected-users-box">
                <div className="upper-box">
                    Connected
                </div>
                <div className="lower-box">
                    <ul>
                        <li>Steffo</li>
                        <li>ciaociao</li>
                        <li>Banana</li>
                        <li>PotatOS</li>
                        <li>Tua mamma</li>
                        <li>Il mifioso</li>
                        <li>That guy</li>
                    </ul>
                </div>
            </div>
        )
    }
}


ReactDOM.render(
    <Client mode="Lobby"/>,
    document.getElementById("react-app")
);