const tokenDiv = document.querySelector("#token_device");

const create_token_device = () => {
  const tokenDeviceBTN: Element | null =
    document.querySelector("#token_device_btn");
  const deviceName: HTMLInputElement | null =
    document.querySelector("#device_name");
  const typeKey: HTMLInputElement | null =
    document.querySelector("#type_of_key");

  tokenDeviceBTN?.addEventListener("click", (event) => {
    event.preventDefault();
    const type_of_key = typeKey?.value;
    const name = deviceName?.value;

    fetch("/auth/token_setup/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({ type_of_key, name }),
    }).then((data) => {
      if (data.ok) {
        data.json().then((d) => {
          const { otp_device, link } = d;
          tokenDiv!.innerHTML = `
          <div id="token_key_div">
            <img id="token_key_qrcode" width="200" height="200" style="background-color: white" src="${link}" />  
                      
            <form action="" id="otp_device_form" method="POST">
              <label htmlfor="id_otp_token">Otp token:</label>
                  <input type="text" name="otp_token" autoComplete="off" id="id_otp_token" />
              <input id="otp_device_form_btn" type="submit" value="submit" />
            </form>
          </div>
          `;
          const otpDeviceForm = document.querySelector("#otp_device_form");
          if (otpDeviceForm) scanSign(otp_device);
        });
      } else {
        data.json().then((e) => console.log(e));
      }
    });
  });
};

if (tokenDiv) create_token_device();

const scanSign = (otp_device: string) => {
  const otpToken: HTMLInputElement | null =
    document.querySelector("#id_otp_token");
  const otpDeviceFormBtn = document.querySelector("#otp_device_form_btn");

  otpDeviceFormBtn?.addEventListener("click", (event) => {
    event.preventDefault();
    const otp_token = parseInt(otpToken!.value);
    const otp_challenge = "";

    fetch("/auth/token_setup/check/", {
      method: "POST",
      headers: headers,
      body: JSON.stringify({ otp_token, otp_challenge, otp_device }),
    }).then((data) => {
      if (data.ok) {
        data.json().then((d) => {
          if (d?.success) {
            const tokenKeyDiv = document.querySelector("#token_key_div");
            tokenKeyDiv!.innerHTML = `
            <p>Correct OTP code!</p>
            `;
            createBackup();
          }
        });
      } else {
        data.json().then((e) => console.log(e));
      }
    });
  });
};

const createBackup = () => {
  const backUpDiv = document.createElement("div");
  backUpDiv.setAttribute("id", "backup_div");
  backUpDiv.innerHTML = `
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
  tokenDiv?.append(backUpDiv);

  const backupCancel = document.querySelector("#backup_cancel");
  const backupGenerate = document.querySelector("#backup_generate");
  const backupCodeDiv = document.querySelector("#backup_code_div");

  backupCancel?.addEventListener("click", (event) => {
    event.preventDefault();
    redirect();
  });
  backupGenerate?.addEventListener("click", (event) => {
    event.preventDefault();
    fetch("/auth/token_setup/backup_code/").then((data) => {
      if (data.ok) {
        data.json().then((d) => {
          let liElems = "";
          d?.codes.forEach((element: string) => {
            liElems += `<li>${element}</li>`;
          });

          backupCodeDiv!.innerHTML = `
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
          const backupDone = document.querySelector("#backup_done");
          backupDone?.addEventListener("click", (event) => {
            event.preventDefault();
            redirect();
          });
        });
      } else {
        data.json().then((e) => console.log(e));
      }
    });
  });
};

const redirect = () => {
  if (window.location.search != "") {
    const redirect_path =
      window.location.search.split("=")[
        window.location.search.split("=").length - 1
      ];
    window.location.href = redirect_path;
  } else window.location.href = "/";
};
