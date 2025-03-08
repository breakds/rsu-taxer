declare module 'react-plotly.js' {
  import { Component } from 'react';

  class Plot extends Component<{
    data?: any[];
    layout?: any;
    style?: any;
    useResizeHandler?: boolean;
  }> { }

  export default Plot;
}
