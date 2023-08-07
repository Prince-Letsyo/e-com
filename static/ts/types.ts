export type DeviceLink = {
  otp_device: string;
  link: string;
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

export type ResponseError = {
  name?: string;
};

export type MainStore = {
  deviceLinkData: {
    device: DeviceLink;
    dataBackup:DataBackup
  };
  siteData: {
    site: DataSite;
  };

};

export type StateChangeFN = (prevState: MainStore) => MainStore;
