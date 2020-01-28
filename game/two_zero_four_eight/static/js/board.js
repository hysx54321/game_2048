export { Board as default } from "./board.js";


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