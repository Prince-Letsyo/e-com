export type DeviceLink = {
  otp_device: string;
  qrcode_link: string;
};

export type DataSuccess = {
  success: boolean;
};

export type DataBackup = {
  codes: string[];
};

export type DataSite = {
  name: string;
  domain: string;
};
export type DataSiteError = {
  name: string[];
  domain: string[];
};

export type ResponseError = {
  name?: string;
};

export type DeviceLinkError = {
  has_other_device: boolean;
  exist: boolean;
};

export type MainStore = {
  deviceLinkData: {
    errors: DeviceLinkError;
    device: DeviceLink;
    dataBackup: DataBackup;
  };
  siteData: {
    errors: DataSiteError;
    site: DataSite;
  };
};

export type StateChangeFN = (prevState: MainStore) => MainStore;
