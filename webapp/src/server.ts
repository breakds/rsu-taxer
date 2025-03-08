const IS_DEV_MODE = import.meta.env.MODE === "development";

const serverUrl = IS_DEV_MODE ? "http://localhost:31415" : (
  `${window.location.protocol}//${window.location.host}`);

export { IS_DEV_MODE, serverUrl };
