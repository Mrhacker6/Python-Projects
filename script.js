const boardElement = document.getElementById("board");
const messageElement = document.getElementById("message");
let board = Array(9).fill("");
let gameOver = false;

const winningCombos = [
  [0,1,2],[3,4,5],[6,7,8],
  [0,3,6],[1,4,7],[2,5,8],
  [0,4,8],[2,4,6]
];

function renderBoard() {
  boardElement.innerHTML = "";
  board.forEach((cell, i) => {
    const cellElement = document.createElement("div");
    cellElement.className = "cell";
    cellElement.innerText = cell;
    cellElement.onclick = () => makeMove(i);
    boardElement.appendChild(cellElement);
  });
}

function makeMove(index) {
  if (board[index] !== "" || gameOver) return;

  board[index] = "X";
  renderBoard();
  if (checkWinner("X")) {
    highlightWinner("X");
    return;
  } else if (isDraw()) {
    endGame("It's a draw!");
    return;
  }

  const aiIndex = bestMove();
  board[aiIndex] = "O";
  renderBoard();

  if (checkWinner("O")) {
    highlightWinner("O");
  } else if (isDraw()) {
    endGame("It's a draw!");
  }
}

function highlightWinner(player) {
  const cells = document.querySelectorAll(".cell");
  for (let combo of winningCombos) {
    if (combo.every(i => board[i] === player)) {
      combo.forEach(i => cells[i].classList.add("winner"));
      endGame(`${player === "X" ? "You" : "AI"} win!`);
      break;
    }
  }
}

function checkWinner(player) {
  return winningCombos.some(combo =>
    combo.every(i => board[i] === player)
  );
}

function isDraw() {
  return board.every(cell => cell !== "");
}

function endGame(message) {
  gameOver = true;
  messageElement.innerText = message;
}

function resetGame() {
  board = Array(9).fill("");
  gameOver = false;
  messageElement.innerText = "";
  renderBoard();
}

function bestMove() {
  let bestScore = -Infinity;
  let move;

  for (let i = 0; i < 9; i++) {
    if (board[i] === "") {
      board[i] = "O";
      let score = minimax(board, 0, false);
      board[i] = "";
      if (score > bestScore) {
        bestScore = score;
        move = i;
      }
    }
  }
  return move;
}

function minimax(boardState, depth, isMaximizing) {
  if (checkWinner("O")) return 1;
  if (checkWinner("X")) return -1;
  if (isDraw()) return 0;

  if (isMaximizing) {
    let bestScore = -Infinity;
    for (let i = 0; i < 9; i++) {
      if (boardState[i] === "") {
        boardState[i] = "O";
        let score = minimax(boardState, depth + 1, false);
        boardState[i] = "";
        bestScore = Math.max(score, bestScore);
      }
    }
    return bestScore;
  } else {
    let bestScore = Infinity;
    for (let i = 0; i < 9; i++) {
      if (boardState[i] === "") {
        boardState[i] = "X";
        let score = minimax(boardState, depth + 1, true);
        boardState[i] = "";
        bestScore = Math.min(score, bestScore);
      }
    }
    return bestScore;
  }
}

renderBoard();
