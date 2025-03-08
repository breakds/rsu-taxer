export interface PlotData {
  x: any[];
  y: any[];
  type?: string;
  mode?: string;
  marker?: any;
  name?: string;
  stackgroup?: string;
  fill?: string;
}


export interface PlotLayout {
  title: string;
  xaxis?: any;
  yaxis?: any;
  autosize: boolean;
}


export interface PlotResponse {
  data: PlotData[];
  layout: PlotLayout;
}
