class Board extends React.Component {
  constructor(props) {
    super(props);
    this.size = props.size;
  }

  renderRow(i) {
    const row = Array(this.size).fill(0).map((item, index) =>
      <button className="square" key={i + ',' + index}>{this.props.board[i][index] == 0 ? null : this.props.board[i][index]}</button>
    );
    return <div className="board-row" key={'row' + i}>{row}</div>;
  }

  render() {
    const rows = Array(this.size).fill(0).map((item, index) =>
      this.renderRow(index)
    );
    return <div>{rows}</div>;
  }
}

class Replayer extends React.Component {
  constructor(props) {
    super(props);
    this.size = 4;
    this.state = {
      move: 0
    };
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.direction = {
      1: "Up",
      2: "Down",
      3: "Left",
      4: "Right"
    };
    this.history = JSON.parse(props.history);
  }

  handleKeyDown(e) {
    var key = e.key;
    switch (key) {
      case "ArrowLeft":
        this.jumpTo(this.state.move - 1);
        // code for "left arrow" key press.
        break;
      case "ArrowRight":
        this.jumpTo(this.state.move + 1);
        // code for "right arrow" key press.
        break;
      default:
        return; // Quit when this doesn't handle the key event.
    }
  }

  jumpTo(move) {
    if (move < 0 || move >= this.history.length) return;
    this.setState({
      move: move
    });
  }

  render() {
    const current = this.history[this.state.move];
    const nextMove = this.state.move == this.history.length ? "No More" : this.direction[this.history[this.state.move + 1].previousMove];
    return (
      <div className="game" onKeyDown={this.handleKeyDown} tabIndex="888" key='game'>
        <div className="game-board"><Board board={current.board} size={this.size} /></div>
        <ul className="game-info">
          <li>{"Score:" + current.score}</li>
          <li>{"Move:" + this.state.move}</li>
          <li>{"Next Move:" + nextMove}</li>
        </ul>
      </div>
    )
  }
}
// ========================================

// ReactDOM.render(<Replayer />, document.getElementById("root"));
//# sourceURL=pen.js
