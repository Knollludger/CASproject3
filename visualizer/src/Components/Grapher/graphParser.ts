export function parseMatrix(matrixString: string) {
  // Split the initial matrix into lines.
  let lines = matrixString.split("\n");

  let matrix = lines.map((line) => line.split(","));

  //   console.log(matrix);
  return matrix;
}

export function parseColors(colorString: string) {
  let colorLines = colorString.split("\n");
  let colors = colorLines.map((line) => line.split(",").map(toColor));
  return colors;
}

function toColor(colorChar: string) {
  switch (colorChar) {
    case "W":
      return "#ffffff";
    case "B":
      return "#000000";
    case "A":
      return "#113399";
    default:
      return "#ba1111";
  }
}

// these cover the intended formats that we are going to be parsing!
// parseMatrixString = `0,1,1,0\n1,0,0,1\n1,0,0,0\n0,1,0,0`;
// let initialColorMatrix = `B,W,B,W`;
// console.log(parseColors(initialColorMatrix));
