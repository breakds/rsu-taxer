import { useState } from 'react'
import './App.css'
import { Segment, Input, Label, Button
} from 'semantic-ui-react'
import Plot from 'react-plotly.js'

function App() {
  const [count, setCount] = useState(0)

  const x = Array.from({ length: 100 }, (_, i) => i / 10);
  const yCurve = x.map((t) => Math.sin(t)); // Curve
  const yArea = x.map((t) => 0.5 * Math.cos(t)); // Area

  const data = [
        {
          x: [1, 2, 3, 4, 5],
          y: [10, 20, 30, 40, 50],
          type: 'scatter',
          mode: 'lines',
          stackgroup: 'one', // Enables stacking
          fill: 'tonexty',
          name: 'Category 1'
        },
        {
          x: [1, 2, 3, 4, 5],
          y: [5, 15, 25, 35, 45],
          type: 'scatter',
          mode: 'lines',
          stackgroup: 'one',
          fill: 'tonexty',
          name: 'Category 2'
        },
        {
          x: [1, 2, 3, 4, 5],
          y: [2, 8, 15, 25, 30],
          type: 'scatter',
          mode: 'lines',
          stackgroup: 'one',
          fill: 'tonexty',
          name: 'Category 3'
        }
  ]

  /* const data = [
   *   {
   *     x: x,
   *     y: yArea,
   *     mode: "lines",
   *     fill: "tozeroy", // Fill area to the x-axis
   *     name: "Area",
   *     line: { color: "rgba(255, 100, 100, 0.5)" },
   *     fillcolor: "rgba(255, 100, 100, 0.5)",
   *   },
   *   {
   *         x: x,
   *         y: yCurve,
   *         mode: "lines",
   *         name: "Curve",
   *         line: { color: "blue" },
   *       },
   * ] */

  return (
    <>
      <Segment color='olive'>
        <div style={{marginBottom: 20}}>
          <Input labelPosition='right' type='text' placeholder='Settlement Price' style={{marginRight: 20}}>
            <Label basic>$</Label>
            <input />
            <Label>Settle</Label>
          </Input>
          <Input labelPosition='right' type='text' placeholder='Settled Shares'>
            <input />
            <Label>Shares</Label>
          </Input>
        </div>
        <div style={{marginBottom: 20}}>
          <Input labelPosition='right' type='text' placeholder='Long term capitcal gain' style={{marginRight: 20}}>
            <Label basic>$</Label>
            <input />
            <Label>Long Term</Label>
          </Input>
          <Input labelPosition='right' type='text' placeholder='Short term capital gain' style={{marginRight: 20}}>
            <Label basic>$</Label>
            <input />
            <Label>Short Term</Label>
          </Input>
        </div>
        <div>
          <Button primary>Run</Button>
        </div>
      </Segment>
      <Segment color="red">
        <Plot data={data}
              layout={{ title: "Curve and Area Graph", height: 600, margin: { t: 30, r: 10, b: 40, l: 50}}}
              style={{width: "100%"}}
              useResizeHandler={true}
        />
      </Segment>
    </>
  )
}

export default App
