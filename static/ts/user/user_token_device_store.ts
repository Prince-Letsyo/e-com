import Store from "../store.js";
import {
  DataBackup,
  DataSuccess,
  DeviceLink,
  DeviceLinkError,
  MainStore,
} from "../types.js";
import { headers } from "../utils.js";

export default class TokenDeviceStore extends Store {
  constructor() {
    super();
  }

  generateTokenBackUp() {
    fetch("/auth/token_setup/backup_code/").then((data: Response) => {
      if (data.ok) {
        data.json().then((dataBackUp: DataBackup) => {
          this.saveState((prevState: MainStore) => {
            prevState.deviceLinkData.dataBackup = dataBackUp;
            return prevState;
          });
          this.dispatchType("token_generate_backup_code");
        });
      } else {
        data.json().then((e) => console.log(e));
      }
    });
  }

  processTokenCode(
    otp_token: number,
    otp_challenge: string,
    otp_device: string
  ) {
    fetch("/auth/token_setup/check/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        otp_token,
        otp_challenge,
        otp_device,
      }),
    }).then((data: Response) => {
      if (data.ok) {
        data.json().then((dataSuccess: DataSuccess) => {
          if (dataSuccess.success) {
            this.saveState((prevState: MainStore) => {
              return prevState;
            });
            this.dispatchType("token_process_token_code");
          }
        });
      } else {
        data.json().then((e) => {
          console.log(e);
        });
      }
    });
  }

  createTokenDevice(type_of_key: string, name: string) {
    fetch("/auth/token_setup/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({ type_of_key, name }),
    }).then((data: Response) => {
      if (data.ok) {
        data.json().then((deviceLink: DeviceLink) => {
          this.saveState((prevState: MainStore) => {
            prevState.deviceLinkData.device = deviceLink;
            return prevState;
          });
          this.dispatchType("token_token_device");
        });
      } else {
        data.json().then((error: DeviceLinkError) => {
          this.saveState((prevState: MainStore) => {
            prevState.deviceLinkData.errors = error;
            return prevState;
          });
          console.log(error);
        });
        this.dispatchType("token_token_device_error");
      }
    });
  }
}
