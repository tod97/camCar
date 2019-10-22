import { Component } from '@angular/core';
import { HttpRequestsService } from '../http-requests.service';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page {

  elements: any = [];
  nameSelected = '';

  constructor(private req: HttpRequestsService) {
  }

  ionViewWillEnter() {
    this.updateData();
  }

  updateData(evt?: any) {
    this.req.getRecordsList()
    .subscribe(data => {
      this.elements = (data['files']) ? data['files'] : [];
      if (evt) { evt.target.complete(); }
     }, error => {
      console.log(error);
      if (evt) { evt.target.complete(); }
    });
  }

  showVideo(name) {
    if (this.nameSelected === name) {
      this.nameSelected = '';
    } else {
      this.nameSelected = name;
    }
  }

}
