import { redirect } from "../utils.js";
import TokenDeviceStore from "./user_token_device_store.js";
import TokenDeviceView from "./user_token_device_view.js";

export default function initTokenApp() {
  const token_device_view = new TokenDeviceView();
  const token_device_store = new TokenDeviceStore();

  token_device_store.addEventListener("token_token_device", (_event: Event) => {
    const { device } = token_device_store.store.deviceLinkData;
    token_device_view.showQrcode(device);
    processTokenCode(token_device_view, token_device_store, device.otp_device);
  });

  token_device_store.addEventListener(
    "token_process_token_code",
    (_event: Event) => {
      token_device_view.createBackUp();
      cancelTokenBackUp(token_device_view);
      generateTokenBackUp(token_device_view, token_device_store);
    }
  );

  token_device_store.addEventListener(
    "token_generate_backup_code",
    (_event: Event) => {
      const { dataBackup } = token_device_store.store.deviceLinkData;
      token_device_view.generatedBackUp(dataBackup);
      doneTokenBackUp(token_device_view);
    }
  );

  createTokenDevice(token_device_view, token_device_store);
}

window.addEventListener("load", initTokenApp);

const createTokenDevice = (view: TokenDeviceView, store: TokenDeviceStore) => {
  view.createTokenDevice("click", (event: Event) => {
    event.preventDefault();
    const type_of_key: string | undefined = view.checkForInputValue(
      view.$.typeKey
    ) as string;
    const name: string | undefined = view.checkForInputValue(
      view.$.deviceName
    ) as string;
    store.createTokenDevice(type_of_key, name);
  });
};

const processTokenCode = (
  view: TokenDeviceView,
  store: TokenDeviceStore,
  otp_device: string
) => {
  view.processTokenCode("click", (event: Event) => {
    event.preventDefault();
    const otp_token: number = parseInt(
      view.checkForInputValue(view.$.otpToken) as string
    );
    store.processTokenCode(otp_token, "", otp_device);
  });
};
const cancelTokenBackUp = (view: TokenDeviceView) => {
  view.cancelTokenBackUp("click", (event: Event) => {
    event.preventDefault();
    redirect();
  });
};

const generateTokenBackUp = (
  view: TokenDeviceView,
  store: TokenDeviceStore
) => {
  view.generateTokenBackUp("click", (event: Event) => {
    event.preventDefault();
    store.generateTokenBackUp();
  });
};

const doneTokenBackUp = (view: TokenDeviceView) => {
  view.doneTokenBackUp("click", (event: Event) => {
    event.preventDefault();
    redirect();
  });
};
