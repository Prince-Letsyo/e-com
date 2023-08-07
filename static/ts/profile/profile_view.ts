import { DataBackup } from "../types.js";
import View from "../views.js";

export default class ProfileView extends View {
  constructor() {
    super();
    this.$.userBackupCodeDiv = this.qs("#user_backup_code_div");
  }

  public generateBackCodes(
    type: string,
    handler: EventListenerOrEventListenerObject
  ): void {
    this.addGenerateBackCodeBTN();
    this.$.backupGenerate.addEventListener(type, handler);
  }
  protected addGenerateBackCodeBTN(): void {
    this.$.userBackupCodeDiv.innerHTML = `<button id="backup_generate">Generate backup codes</button>`;
    this.$.backupGenerate = this.qs("#backup_generate");
  }

  public generateBacUpCode(dataBackUp: DataBackup){
    let liElems = "";
    dataBackUp.codes.forEach((element: string) => {
      liElems += `<li>${element}</li>`;
    });
    this.$.userBackupCodeDiv.innerHTML = `
    <div id="generated_code_div">
      <p>
        Copy the back up codes and store it in a secure place. 
        Each token code expires after use.
        You can generate new backup codes on your Profile dashboard.
      </p>
      <ul>
      ${liElems}
      </ul>
    </div>
    <button id="backup_done">Done</button>
    `;
  }
}
