import { MainStore, StateChangeFN } from "./types";

let initialStore: MainStore = {
  siteData: {
    site: {
      domain: "",
      name: "",
    },
    errors: {
      name: [],
      domain: []
    }
  },
  deviceLinkData: {
    device: {
      otp_device: "",
      link: "",
    },
    dataBackup: {
      codes: [],
    },
    errors: {
      has_other_device: false,
      exist: false
    },
  },
};

export default class Store extends EventTarget {
  constructor() {
    super();
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
    console.log(initialStore);
  }
  protected dispatchType(type: string): void {
    this.dispatchEvent(new Event(type));
  }
}
