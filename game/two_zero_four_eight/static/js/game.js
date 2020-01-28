
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function httpPost(URL, PARAMS) {
  var form = document.createElement("form");
  form.action = URL;
  form.method = "POST";
  form.style.display = "none";
  for (var key in PARAMS) {
    var field = document.createElement("textarea");
    field.name = key;
    field.value = PARAMS[key];
    form.appendChild(field);
  }
  document.body.appendChild(form);
  form.submit();
  return form;
}

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

function emptyMatrix(numRow, numCol) {
  var arr = [];
  for (var i = 0; i < numRow; ++i) {
    var columns = [];
    for (var j = 0; j < numCol; ++j) {
      columns[j] = 0;
    }
    arr[i] = columns;
  }
  return arr;
}

function cloneMatrix(matrix) {
  var newMatrix = [];
  for (var i = 0; i < matrix.length; ++i) {
    var columns = [];
    for (var j = 0; j < matrix[0].length; ++j) {
      columns[j] = matrix[i][j];
    }
    newMatrix[i] = columns;
  }
  return newMatrix;
}

function copyMatrix(matrix, target) {
  for (var i = 0; i < target.length; ++i) {
    for (var j = 0; j < target[0].length; ++j) {
      matrix[i][j] = target[i][j];
    }
  }
}

function rotateClockwise(matrix) {
  var newMatrix = emptyMatrix(matrix[0].length, matrix.length);
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[0].length; j++) {
      newMatrix[j][matrix[0].length - 1 - i] = matrix[i][j];
    }
  }
  copyMatrix(matrix, newMatrix);
  // matrix = newMatrix;
  // return newMatrix;
}

function rotateAntiClockwise(matrix) {
  var newMatrix = emptyMatrix(matrix[0].length, matrix.length);
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[0].length; j++) {
      newMatrix[matrix.length - 1 - j][i] = matrix[i][j];
    }
  }
  copyMatrix(matrix, newMatrix);
  // matrix = newMatrix;
  // return newMatrix;
}

function reflect(matrix) {
  var newMatrix = emptyMatrix(matrix.length, matrix[0].length);
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[0].length; j++) {
      newMatrix[i][matrix[0].length - 1 - j] = matrix[i][j];
    }
  }
  copyMatrix(matrix, newMatrix);
  // matrix = newMatrix;
  // return newMatrix;
}

function merge(matrix) {
  var score = 0;
  var move = 0;
  move += moveToLeft(matrix);
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 1; j < matrix[0].length; j++) {
      if (matrix[i][j - 1] == matrix[i][j]) {
        score += matrix[i][j];
        matrix[i][j - 1] *= 2;
        matrix[i][j] = 0;
      }
    }
  }
  move += moveToLeft(matrix);
  return { score: score, move: move };
}

function moveToLeft(matrix) {
  var move = 0;
  for (let i = 0; i < matrix.length; i++) {
    var index = 0;
    for (let j = 0; j < matrix[0].length; j++) {
      if (matrix[i][j] != 0) {
        if (j == index) {
          index++;
          continue;
        }
        move++;
        matrix[i][index++] = matrix[i][j];
        matrix[i][j] = 0;
      }
    }
  }
  return move;
}

var test = [
  [2, 4, 4, 8],
  [4, 16, 32, 4],
  [2, 16, 128, 4],
  [4, 2, 2, 4]
];

var test = [
  [16, 8, 4, 2],
  [64, 32, 16, 4],
  [128, 64, 32, 8],
  [2, 32, 16, 2]
];

function up(matrix) {
  rotateAntiClockwise(matrix);
  var result = merge(matrix);
  rotateClockwise(matrix);
  return result;
}

function down(matrix) {
  rotateClockwise(matrix);
  var result = merge(matrix);
  rotateAntiClockwise(matrix);
  return result;
}

function left(matrix) {
  var result = merge(matrix);
  return result;
}

function right(matrix) {
  reflect(matrix);
  var result = merge(matrix);
  reflect(matrix);
  return result;
}

function isEndGame(matrix) {
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[0].length; j++) {
      if (matrix[i][j] == 0) return false;
      if (i != 0 && matrix[i - 1][j] == matrix[i][j]) return false;
      if (i != matrix.length - 1 && matrix[i + 1][j] == matrix[i][j]) return false;
      if (j != 0 && matrix[i][j - 1] == matrix[i][j]) return false;
      if (j != matrix[0].length - 1 && matrix[i][j + 1] == matrix[i][j]) return false;
    }
  }
  console.log(matrix);
  console.log("Game ends");
  return true;
}

function addRandom(matrix) {
  var random = Math.floor((Math.random() * 10) + 1);
  var number = random == 1 ? 4 : 2;
  do {
    var row = Math.floor((Math.random() * matrix.length));
    var col = Math.floor((Math.random() * matrix.length));
  }
  while (matrix[row][col] != 0);
  matrix[row][col] = number;
}

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.size = 4;
    this.state = {
      gameStarted: false,
      board: emptyMatrix(this.size, this.size),
      message: "Click 'Start' to start the game"
    };
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.startGame = this.startGame.bind(this);
    this.endGame = this.endGame.bind(this);
    this.saveGame = this.saveGame.bind(this);
    this.updateTime = this.updateTime.bind(this);
    this.undo = this.undo.bind(this);
    this.direction = {
      Up: 1,
      Down: 2,
      Left: 3,
      Right: 4
    };
  }

  startGame() {
    var board = emptyMatrix(this.size, this.size);
    addRandom(board);
    this.timer = setInterval(this.updateTime, 1000);
    this.setState({
      history: [
        {
          board: board,
          score: 0,
          previousMove: null
        }],
      board: board,
      gameStarted: true,
      gameEnds: false,
      score: 0,
      move: 0,
      uselessMove: 0,
      message: "The game has started. Good luck!",
      second: 0
    });
  }

  endGame() {
    this.setState({
      gameEnds: true,
      message: "The game has been terminated.",
    })
    this.saveGame();
  }

  updateTime() {
    if (this.state.gameEnds) {
      clearInterval(this.timer);
      return;
    }
    this.setState({
      second: this.state.second + 1
    })
  }

  saveGame() {
    console.log("This is the end of the game");
    console.log(this.state);
    var history = JSON.stringify(this.state.history);
    // var obj = JSON.parse(history);
    // console.log(obj);
    var csrftoken = getCookie('csrftoken');
    httpPost(
      "../save_game/",
      {
        second: this.state.second,
        score: this.state.score,
        move: this.state.move,
        useless_move: this.state.uselessMove,
        reconstruction: history,
        csrfmiddlewaretoken: csrftoken
      }
    );
  }

  undo() {
    var history = this.state.history;
    if (history.length == 1) return;
    history.pop();
    var current = history[history.length - 1];
    this.setState({
      history: history,
      board: current.board,
      score: current.score,
      move: history.length - 1
    })
  }

  handleKeyDown(e) {
    if (this.state.gameStarted && this.state.gameEnds) return;
    var key = e.key;
    // console.log(e.key);
    var board = cloneMatrix(this.state.board);
    var result;
    var move;
    switch (key) {
      case "ArrowUp":
        move = this.direction.Up;
        result = up(board);
        // code for "down arrow" key press.
        break;
      case "ArrowDown":
        move = this.direction.Down;
        result = down(board);
        // code for "up arrow" key press.
        break;
      case "ArrowLeft":
        move = this.direction.Left;
        result = left(board);
        // code for "left arrow" key press.
        break;
      case "ArrowRight":
        move = this.direction.Right;
        result = right(board);
        // code for "right arrow" key press.
        break;
      case "z":
        this.undo();
        return;
      default:
        return; // Quit when this doesn't handle the key event.
    }

    if (result.score == 0 && result.move == 0) {
      this.setState({
        uselessMove: this.state.uselessMove + 1
      });
      return;
    }

    addRandom(board);

    let gameEnd = isEndGame(board);
    var message;
    if (gameEnd) {
      message = "Game ends";
    } else {
      message = "Keep playing";
    }

    var history = this.state.history;
    var score = this.state.score + result.score;
    history.push({
      board: board,
      score: score,
      previousMove: move
    });

    this.setState({
      history: history,
      board: board,
      gameEnds: gameEnd,
      score: score,
      message: message,
      move: this.state.move + 1
    });

    if (gameEnd) this.saveGame();
  }

  render() {
    var board = this.state.board;
    var message = this.state.message;
    var scoreBoard = this.state.gameStarted ? <li>{"Score:" + this.state.score}</li> : null;
    var moveBoard = this.state.gameStarted ? <li>{"Move:" + this.state.move}</li> : null;
    var uselessMoveBoard = this.state.gameStarted ? <li>{"Useless move:" + this.state.uselessMove}</li> : null;
    var timer = this.state.gameStarted ? <li>{"Second:" + this.state.second}</li> : null;
    var startButton = this.state.gameEnds || !this.state.gameStarted ? <button className="start" onClick={this.startGame}>Start</button> : null;
    var endButton = this.state.gameStarted && !this.state.gameEnds ? <button className="end" onClick={this.endGame}>End Game</button> : null;
    var undoButton = this.state.gameStarted && !this.state.gameEnds ? <button className="undo" onClick={this.undo}>Undo</button> : null;

    //var saveGameForm = this.state.gameEnds ? React.createElement("form", { className: "save", onClick: this.startGame }, "Start") : "";
    return (
      <div className="game" onKeyDown={this.handleKeyDown} tabIndex="888" key='game'>
        <div className="game-board"><Board board={board} size={this.size} /></div>
        <ul className="game-info">
          <p className="message">{message}</p>
          {scoreBoard}
          {moveBoard}
          {uselessMoveBoard}
          {timer}
          <div className="buttons">
            {startButton}
            {endButton}
            {undoButton}
          </div>
        </ul>
      </div>
    )
  }
}
// ========================================

ReactDOM.render(<Game />, document.getElementById("root"));
//# sourceURL=pen.js
