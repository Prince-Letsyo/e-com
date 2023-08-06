import { DataSite } from "../types.js";
import View from "../views.js";

export default class SiteView extends View {
  update_url: string;
  create_url: string;
  constructor() {
    super();
    try {
      this.$.siteForm = this.qs("#create_site");
      this.createSite();
    } catch (error) {
      console.log({error});
    }
    this.$.websiteDiv = this.qs("#website_div");
    this.update_url = `/auth/update_domain/`;
    this.create_url = `/auth/create_domain/`;
  }

  public submitSite(
    type: string,
    handler: EventListenerOrEventListenerObject
  ): void {
    try {
      this.$.siteBtn.addEventListener(type, handler);
    } catch (error) {
        this.fetchSite();
    }
  }

  public editSubmitedSite(
    type: string,
    handler: EventListenerOrEventListenerObject
  ): void {
    this.$.editSite.addEventListener(type, handler);
  }

  public createSite() {
    this.$.siteBtn = this.qs("#submit_site");
    this.$.domainName = this.qs("#domain_name");
    this.$.displayName = this.qs("#display_name");
  }

  public reCreateSite(dataSite: DataSite) {
    this.$.websiteDiv.innerHTML = `
    <form id="create_site" method="POST">
      <label htmlFor="domain_name">Domain Name</label>
      <input type="text" value="${dataSite.domain}" id="domain_name" placeholder="http://www.example.com" />
      <br />
      <br />
      <label htmlFor="display_name">Display Name</label>
      <input type="text" value="${dataSite.name}" id="display_name" placeholder="www.example.com" />
      <br />
      <br />
      <input type="submit" id="submit_site" />
    </form>`;
  }

  public displaySite(dataSite: DataSite): void {
    this.$.websiteDiv.innerHTML = `<div id="website_name" />
      <p><span>Website: </span>${dataSite.name}</p>
      <button id="edit_site">Edit</button> 
      </div>`;

    this.$.editSite = this.qs("#edit_site");
    this.fetchSite(this.$.editSite as HTMLInputElement);
  }

  private fetchSite(editSite?: HTMLInputElement): void {
    if (!editSite) this.$.editSite = this.qs("#edit_site");
  }
}
