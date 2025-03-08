import { useState } from 'react'
import './App.css'
import { Segment, Input, Label, Button
} from 'semantic-ui-react'

function App() {
  const [count, setCount] = useState(0)

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
      </Segment>
    </>
  )
}

export default App
