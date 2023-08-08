import Store from "../store.js";
import { DataBackup, DeviceLinkError, MainStore } from "../types.js";

export default class ProfileStore extends Store {
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
        data.json().then((error) => {
          console.log(error);
        });
      }
    });
  }

  checkNumberOfBackUpCodes() {
    fetch("/auth/user_backup_code/").then((data: Response) => {
      if (data.ok) {
        data.json().then((dataBackUp: DataBackup) => {
          this.saveState((prevState: MainStore) => {
            prevState.deviceLinkData.dataBackup = dataBackUp;
            return prevState;
          });
          this.dispatchType("token_user_backup_code");
        });
      } else {
        data.json().then((error: DeviceLinkError) => {
          this.saveState((prevState: MainStore) => {
            prevState.deviceLinkData.errors = error;
            return prevState;
          });
          console.log(error);
          this.dispatchType("token_user_backup_code_error");
        });
      }
    });
  }
}
