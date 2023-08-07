import { MainStore, StateChangeFN } from "./types";

let initialStore: MainStore = {
  siteData: {
    site: {
      domain: "",
      name: "",
    },
  },
  deviceLinkData: {
    device: {
      otp_device: "",
      link: "",
    },
    dataBackup: {
      codes: [],
    },
  },
};

export default class Store extends EventTarget {
  constructor() {
    super();
    // setTimeout(() => {
    //   console.log("Up");
    // }, 1000);

    // setInterval(() => {
    //   console.log("Down");
    // }, 1000);
  }

  get store(): MainStore {
    return this.getState();
  }

  protected getState(): MainStore {
    return initialStore;
  }

  protected saveState(stateOrCb: MainStore | StateChangeFN) {
    const prevState: MainStore = this.getState();
    let newState: MainStore;
    switch (typeof stateOrCb) {
      case "function":
        newState = stateOrCb(prevState);
        break;
      case "object":
        newState = stateOrCb;
        break;
      default:
        throw new Error("Invalid arguement passed to saveState");
    }
    initialStore = newState;
  }
}
