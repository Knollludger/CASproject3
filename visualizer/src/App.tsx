import React from "react";
import Field from "./Components/Field";
import "./App.css";
import ThrowsMenu from "./Components/ThrowLayout/ThrowsMenu";
import * as ULT from "./Interfaces";

const App = () => {
  const [matrix, setMatrix] = React.useState<Array<Array<string>>>([[]]);
  const [colors, setColors] = React.useState<Array<Array<string>>>([[]]);
  const [nodes, setNodes] = React.useState<Array<ULT.Node>>([]);
  const [index, setIndex] = React.useState<number>(0);
  const [useRectangles, setUseRectangles] = React.useState<boolean>(false);

  const setAllThree = (matrix, colors, nodes) => {
    // console.log(matrix);
    // console.log(colors);
    setMatrix(matrix);
    setColors(colors);
    setNodes(nodes);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Time Step: {index}</h1>
        <div className="App-Body">
          <Field
            index={index}
            connectionMatrix={matrix}
            nodes={nodes}
            setNodes={setNodes}
            colors={colors}
            useRectangles={useRectangles}
          />
          <ThrowsMenu
            setAllThree={setAllThree}
            setIndex={setIndex}
            setUseRectangles={setUseRectangles}
          />
        </div>
      </header>
    </div>
  );
};

export default App;
