const fs = require("fs");

function toColor(colorChar) {
  switch (colorChar) {
    case "W":
      return "#ffffff";
    case "B":
      return "#000000";
    default:
      return "#ba1111";
  }
}

try {
  const data = fs.readFileSync("./runMatrix100x100.txt", "utf8");
  let timesteps = data.trim().split(":");
  timesteps = timesteps.map((arr) => arr.trim().split("\r\n"));
  timesteps = timesteps.map((arr) =>
    arr.map((x) =>
      x
        .trim()
        .split(",")
        .map((y) => toColor(y.trim()))
    )
  );
  fs.writeFileSync("test100x100.json", JSON.stringify(timesteps, null, 2));
  //file written successfully
  console.log(timesteps.length);
} catch (err) {
  console.error(err);
}
