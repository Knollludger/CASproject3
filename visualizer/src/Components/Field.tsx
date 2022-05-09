import { Stage, Layer, Circle, Line, Rect } from "react-konva";
import "../App.css";
import * as ULT from "../Interfaces";
import React from "react";

interface FieldProps {
  connectionMatrix: Array<Array<string>>;
  colors: Array<Array<string>>;
  nodes: Array<ULT.Node>;
  index: number;
  useRectangles: boolean;
  setNodes: (nodes: Array<ULT.Node>) => void;
}

const Field = (props: FieldProps) => {
  let nodes = props.nodes;

  // const [nodes, setNodes] = React.useState<Array<ULT.Node>>(props.nodes);
  const makeLines = (nodes) => {
    if (props.connectionMatrix.length > 0) {
      let lines: Array<Array<number>> = [];
      for (let i = 0; i < nodes.length; i++) {
        for (let j = 0; j < nodes.length; j++) {
          if (i < j && props.connectionMatrix[i][j] === "1") {
            lines.push([nodes[i].x, nodes[i].y, nodes[j].x, nodes[j].y]);
          }
        }
      }
      return lines;
    } else {
      return [];
    }
  };
  let lines = !props.useRectangles ? makeLines(nodes) : [];
  const ondrag = (e: any) => {
    const target = e.target;
    const id = e.target.id();

    let NewNodes = nodes.map((star) => {
      if (parseInt(star.id) === parseInt(id)) {
        return {
          ...star,
          x: target.attrs.x,
          y: target.attrs.y,
        };
      } else {
        return star;
      }
    });
    props.setNodes(NewNodes);
  };

  const pointHandleClick = (e: any) => {
    const id = e.target.id();
    let tempStars = nodes.map((star) => {
      if (star.id === id) {
        return {
          ...star,
        };
      } else {
        return star;
      }
    });

    props.setNodes(tempStars);
  };

  const handleDragStart = (e: any) => {
    const id = e.target.id();
    let tempNodes = nodes.map((star) => {
      return {
        ...star,
        isDragging: star.id === id,
      };
    });
    props.setNodes(tempNodes);
  };
  const handleDragEnd = (e: any) => {
    let tempNodes = nodes.map((star) => {
      return {
        ...star,
        isDragging: false,
      };
    });
    props.setNodes(tempNodes);
  };
  // const StagehandleClick = (e) => {
  //   let stage = e.target.getStage();
  //   const emptySpace = stage.getPointerPosition();
  //   if (stars.length < 2) {
  //     let tempstars = stars.concat({
  //       id: stars.length.toString(),
  //       x: emptySpace.x,
  //       y: emptySpace.y,
  //       isDragging: false,
  //       color: "#11",
  //     });
  //     stars = tempstars;
  //     // setStars(tempstars);
  //   }
  //   props.setNodes(stars);
  // };

  let width: number = 1200;
  // let height: number = 1500 * 0.4 * 0.8;
  let height: number = 150;
  console.log(props.useRectangles);

  let divisor = props.colors.length > 0 ? props.colors[0].length : 1;
  let rectWidth = width / divisor;
  let rectHeight = height;
  let oneD = true;
  return (
    <div>
      <Stage width={width} height={height} style={{ border: "2px solid gray" }}>
        <Layer>
          {lines.map((line) => (
            <Line
              key={Math.random() * 1000000}
              points={line}
              stroke="white"
              strokeWidth={2}
            />
          ))}
          {!props.useRectangles && oneD
            ? props.nodes.map((star, index) => (
                <Circle
                  key={star.id}
                  id={star.id}
                  x={star.x}
                  y={star.y}
                  radius={20}
                  fill={props.colors[props.index][index]}
                  opacity={0.8}
                  draggable
                  shadowColor="black"
                  shadowBlur={10}
                  shadowOpacity={0.6}
                  shadowOffsetX={star.isDragging ? 10 : 5}
                  shadowOffsetY={star.isDragging ? 10 : 5}
                  scaleX={star.isDragging ? 1.2 : 1}
                  scaleY={star.isDragging ? 1.2 : 1}
                  onDragStart={handleDragStart}
                  onDragEnd={handleDragEnd}
                  onClick={pointHandleClick}
                  onDragMove={ondrag}
                />
              ))
            : props.colors[props.index].map((color, index) => (
                <Rect
                  key={index}
                  x={index * rectWidth}
                  y={0}
                  height={rectHeight}
                  width={rectWidth}
                  fill={color}
                  stroke={"black"}
                  strokeWidth={2}
                />
              ))}
        </Layer>
      </Stage>
    </div>
  );
};

//   return (
//     <div>
//       <Stage width={width} height={height} style={{ border: "2px solid gray" }}>
//         <Layer>
//           {lines.map((line) => (
//             <Line
//               key={Math.random() * 1000000}
//               points={line}
//               stroke="white"
//               strokeWidth={2}
//             />
//           ))}
//           {props.colors[props.index].map((FullArray, outerIndex) =>
//             FullArray.map((color, InnerIndex) => (
//               <Rect
//                 key={outerIndex + InnerIndex}
//                 x={InnerIndex * rectWidth}
//                 y={rectHeight * outerIndex}
//                 height={rectHeight}
//                 width={rectWidth}
//                 fill={color}
//                 stroke={"black"}
//                 strokeWidth={2}
//               />
//             ))
//           )}
//         </Layer>
//       </Stage>
//     </div>
//   );
// };

export default Field;
