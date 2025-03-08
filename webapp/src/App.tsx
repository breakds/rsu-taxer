import { useState } from 'react'
import './App.css'
import { Segment, Input, Label, Button
} from 'semantic-ui-react'
import Plot from 'react-plotly.js'
import { serverUrl } from './server'
import { PlotResponse } from './protocols'


function App() {
  const [ pnl, setPnl ] = useState<PlotResponse | null>(null)

  const fetchPnl = async() => {
    try {
      const response = await fetch(`${serverUrl}/pnl`)
      const payload: Product[] = await response.json()
      setPnl(payload)
    } catch (error) {
      // TODO: prompt to better handle the error
      console.error("Error while fetching products and dates: ", error)
    }
  }

  useEffect(fetchPnl, [])

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
        {pnl && <Plot data={pnl.data}
                      layout={{...pnl.layout, height: 600}}
                      style={{width: "100%"}}
                      useResizeHandler={true}
                />}
      </Segment>
    </>
  )
}

export default App
