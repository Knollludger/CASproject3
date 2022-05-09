import React, { useRef } from "react";
import { Collapse } from "react-bootstrap";
import { Button } from "react-bootstrap";
import { FaCaretDown, FaCaretUp } from "react-icons/fa";
import { parseMatrix, parseColors } from "../Grapher/graphParser";
import * as ULT from "../../Interfaces";

interface ThrowsMenuProps {
  setAllThree: (
    matrix: Array<Array<string>>,
    colors: Array<Array<string>> | Array<Array<Array<string>>>,
    nodes: Array<ULT.Node>
  ) => void;
  setIndex: (num: number) => void;
  setUseRectangles: (bool: boolean) => void;
}

const ThrowsMenu = (props: ThrowsMenuProps) => {
  const [open, setOpen] = React.useState<boolean>(true);
  // eslint-disable-next-line
  const [rows, setRows] = React.useState<number>(10);
  const intervalID = useRef<NodeJS.Timeout>();

  const [matrixVal, setMatrixVal] = React.useState<string>("");
  const [colorsVal, setColorsVal] = React.useState<string>("");
  const [useRects, setUseRects] = React.useState<boolean>(false);
  let style = {
    paddingLeft: "5px",
    paddingBottom: "2px",
    fontSize: "1.5rem",
  };

  const handleColorChange = (event) => {
    setColorsVal(event.target.value);
  };

  const handleMatrixVal = (event) => {
    setMatrixVal(event.target.value);
  };

  const setRect = () => {
    props.setUseRectangles(!useRects);
    setUseRects(!useRects);
  };

  const go = () => {
    console.log("hewwo");
    let parsedMatrix = parseMatrix(matrixVal);
    let parsedColors = parseColors(colorsVal);
    let nodes = parsedColors[0].map((color) => {
      return {
        x: Math.floor(Math.random() * 500),
        y: Math.floor(Math.random() * 500),
        isDragging: false,
        color: color,
        id: "" + Math.floor(Math.random() * 10000000),
      };
    });
    props.setAllThree(parsedMatrix, parsedColors, nodes);

    if (intervalID.current !== undefined) {
      clearInterval(intervalID.current);
    }
    let index = 0;
    props.setIndex(index);

    intervalID.current = setInterval(function () {
      index++;
      let setter = index % (parsedColors.length - 1);
      console.log("hello! " + setter);
      props.setIndex(setter);
    }, 750);
    return;
  };

  return (
    <div className="throws-menu" style={{ display: "inline-block" }}>
      <div>
        <span style={style}>Inputs</span>
        {!open ? (
          <FaCaretDown
            onClick={() => setOpen(!open)}
            aria-controls="example-collapse-text"
            aria-expanded={open}
            size={28}
            className="throws-icon"
          />
        ) : (
          <FaCaretUp
            onClick={() => setOpen(!open)}
            aria-controls="example-collapse-text"
            aria-expanded={open}
            size={28}
            className="throws-icon"
          />
        )}
      </div>
      <Collapse in={open}>
        <div
          style={{
            borderTop: "2px solid gray",
            alignItems: "stretch",
            display: "inline-flex",
            width: "100%",
          }}
        >
          <textarea
            rows={rows}
            cols={50}
            placeholder={"matrix input..."}
            value={matrixVal}
            onChange={handleMatrixVal}
          />
          <textarea
            rows={rows}
            cols={50}
            placeholder={"color sequence input..."}
            value={colorsVal}
            onChange={handleColorChange}
          />
          <div style={{ width: "100%" }}>
            <Button style={{ width: "100%" }} onClick={go}>
              Go!
            </Button>
            <label>
              <input type="checkbox" checked={useRects} onChange={setRect} />
              Rectangles?
            </label>
          </div>
        </div>
      </Collapse>
    </div>
  );
};

export default ThrowsMenu;
