import { MainStore, StateChangeFN } from "./types";

const initialStore: MainStore = {
  siteData: {
    type: "",
    site: {
      domain: "",
      name: "",
    },
  },
  deviceLinkData: {
    type: "",
    device: {
      otp_device: "",
      link: "",
    },
    dataBackup: {
      codes: []
    }
  },
};

export default class Store extends EventTarget {
  private state: MainStore;
  constructor() {
    super();
    this.state = initialStore;
  }

  get store(): MainStore {
    return this.getState();
  }

  protected getState(): MainStore {
    return this.state;
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
    this.state = newState;
    this.dispatchEvent(new Event("statechange"));
  }
}
