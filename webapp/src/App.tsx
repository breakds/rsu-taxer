import { useState, useEffect } from 'react'
import './App.css'
import { Segment, Input, Label, Button
} from 'semantic-ui-react'
import Plot from 'react-plotly.js'
import { serverUrl } from './server'
import { PlotResponse } from './protocols'


function App() {
  const [ pnl, setPnl ] = useState<PlotResponse | null>(null)
  const [ settlement, setSettlement ] = useState<string>("15.0")
  const [ shares, setShares ] = useState<string>("10000")
  const [ longTerm, setLongTerm ] = useState<string>("100000.0")
  const [ shortTerm, setShortTerm ] = useState<string>("50000.0")

  const fetchPnl = async() => {
    try {
      const response = await fetch(`${serverUrl}/pnl?settlement=${settlement}&shares=${shares}&longterm=${longTerm}&shorterm=${shortTerm}`)
      const payload: Product[] = await response.json()
      setPnl(payload)
    } catch (error) {
      // TODO: prompt to better handle the error
      console.error("Error while fetching: ", error)
    }
  }

  useEffect(() => { fetchPnl() }, [])

  const onSetSettlement = (event) => {
    const value = event.target.value
    if (!isNaN(Number(value))) {
      setSettlement(event.target.value)
    }
  }

  const onSetShares = (event) => {
    const value = event.target.value
    if (!isNaN(Number(value))) {
      setShares(event.target.value)
    }
  }

  const onSetLongTerm = (event) => {
    const value = event.target.value
    if (!isNaN(Number(value))) {
      setLongTerm(event.target.value)
    }
  }

  const onSetShortTerm = (event) => {
    const value = event.target.value
    if (!isNaN(Number(value))) {
      setShortTerm(event.target.value)
    }
  }

  return (
    <>
      <Segment color='olive'>
        <div style={{marginBottom: 20}}>
          <Input labelPosition='right'
                 type='number'
                 step={0.1}
                 placeholder='Settlement Price'
                 value={settlement}
                 onChange={onSetSettlement}
                 style={{marginRight: 20}}>
            <Label basic>$</Label>
            <input />
            <Label>Settle</Label>
          </Input>
          <Input labelPosition='right'
                 type='number'
                 step={10000}
                 value={shares}
                 onChange={onSetShares}
                 placeholder='Settled Shares'>
            <input />
            <Label>Shares</Label>
          </Input>
        </div>
        <div style={{marginBottom: 20}}>
          <Input labelPosition='right'
                 type='number'
                 step={10000}
                 value={longTerm}
                 onChange={onSetLongTerm}
                 placeholder='Long term capitcal gain'
                 style={{marginRight: 20}}>
            <Label basic>$</Label>
            <input />
            <Label>Long Term</Label>
          </Input>
          <Input labelPosition='right'
                 type='number'
                 step={10000}
                 placeholder='Short term capital gain'
                 value={shortTerm}
                 onChange={onSetShortTerm}
                 style={{marginRight: 20}}>
            <Label basic>$</Label>
            <input />
            <Label>Short Term</Label>
          </Input>
        </div>
        <div>
          <Button primary onClick={fetchPnl}>Run</Button>
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
