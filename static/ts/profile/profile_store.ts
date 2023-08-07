import Store from "../store.js";
import { DataBackup, MainStore } from "../types.js";

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
          this.dispatchEvent(new Event("token_generate_backup_code"));
        });
      } else {
        data.json().then((e) => console.log(e));
      }
    });
  }
  
  checkNumberOfBackUpCodes(){
    fetch("/auth/user_backup_code/").then((data: Response) => {
      if (data.ok) {
        data.json().then((dataBackUp: DataBackup) => {
          this.saveState((prevState: MainStore) => {
            prevState.deviceLinkData.dataBackup = dataBackUp;
            return prevState;
          });
          this.dispatchEvent(new Event("token_user_backup_code"));
        });
      } else {
        data.json().then((e) => console.log(e));
      }
    });
  }
}
