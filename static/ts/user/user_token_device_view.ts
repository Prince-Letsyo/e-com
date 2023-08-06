import View from "../views.js";
import { DataBackup, DeviceLink } from "../types.js";

export default class TokenDeviceView extends View {
    
  constructor() {
    super();
    this.$.tokenDiv = this.qs("#token_device");

    if (this.$.tokenDiv) this.createToken();
  }

  public createTokenDevice(
    type: string,
    handler: EventListenerOrEventListenerObject
  ): void {
    this.$.tokenDeviceBTN.addEventListener(type, handler);
  }

  public processTokenCode(
    type: string,
    handler: EventListenerOrEventListenerObject
  ): void {
    this.$.otpDeviceFormBtn.addEventListener(type, handler);
  }

  public cancelTokenBackUp(
    type: string,
    handler: EventListenerOrEventListenerObject
  ): void {
    this.$.backupCancel.addEventListener(type, handler);
  }

  public generateTokenBackUp(
    type: string,
    handler: EventListenerOrEventListenerObject
  ): void {
    this.$.backupGenerate.addEventListener(type, handler);
  }
  public doneTokenBackUp(
    type: string,
    handler: EventListenerOrEventListenerObject
  ): void {
    this.$.backupDone.addEventListener(type, handler);
  }

  private createToken(): void {
    this.$.tokenDeviceBTN = this.qs("#token_device_btn");
    this.$.deviceName = this.qs("#device_name");
    this.$.typeKey = this.qs("#type_of_key");
  }

  public showQrcode(deviceLink: DeviceLink): void {
    this.$.tokenDiv.innerHTML = `
    <div id="token_key_div">
    <img id="token_key_qrcode" width="200" height="200" style="background-color: white" src="${deviceLink.link}" />  
    
    <form action="" id="otp_device_form" method="POST">
    <label htmlfor="id_otp_token">Otp token:</label>
    <input type="text" name="otp_token" autoComplete="off" id="id_otp_token" />
    <input id="otp_device_form_btn" type="submit" value="submit" />
    </form>
    </div>
    `;
    this.$.otpDeviceForm = this.qs("#otp_device_form");
    if (this.$.otpDeviceForm) this.scanAndProvideCode(deviceLink.otp_device);
  }

  private scanAndProvideCode(otp_device: string): void {
    this.$.otpToken = this.qs("#id_otp_token");
    this.$.otpDeviceFormBtn = this.qs("#otp_device_form_btn");
  }

  public createBackUp(): void {
    this.$.tokenKeyDiv = this.qs("#token_key_div");
    this.$.tokenKeyDiv.innerHTML = `
    <p>Correct OTP code!</p>
    `;

    this.$.tokenKeyDiv = this.qs("#token_key_div");

    this.$.backUpDiv = this.createElem("div");
    this.$.backUpDiv.setAttribute("id", "backup_div");
    this.$.backUpDiv.innerHTML = `
    <h3 >Back up codes</h3>
    <div id="backup_code_div">
        <p id="backup_text" class="">
          These are frequently used as emergency tokens
          in case a user's normaldevice is lost or unavailable
        </p>
        <div id="bacup_btn_div">
          <button id="backup_cancel">Cancel</button>
          <button id="backup_generate">Generate codes</button> 
        </div>
    </div>
    `;

    this.$.tokenDiv?.append(this.$.backUpDiv);

    this.$.backupCancel = this.qs("#backup_cancel");
    this.$.backupGenerate = this.qs("#backup_generate");
    this.$.backupCodeDiv = this.qs("#backup_code_div");
  }

  public generatedBackUp(dataBackUp:DataBackup):void{
    let liElems = "";
    dataBackUp.codes.forEach((element: string) => {
      liElems += `<li>${element}</li>`;
    });

    this.$.backupCodeDiv.innerHTML = `
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
    this.$.backupDone = this.qs("#backup_done");
  }
}
