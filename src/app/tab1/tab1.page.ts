import { Component } from '@angular/core';

import { HttpRequestsService } from '../http-requests.service';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {

  constructor(private req: HttpRequestsService) { }

  ionViewDidEnter() { }

  connect() {
    this.req.socketConnect();
  }

  disconnect() {
    this.req.socketDisconnect();
  }
}
