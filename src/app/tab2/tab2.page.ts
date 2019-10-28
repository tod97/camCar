import { Component } from '@angular/core';
import { HttpRequestsService } from '../http-requests.service';

import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page {

  elements: any = [];
  nameSelected = '';

  constructor(
    private req: HttpRequestsService,
    public alertController: AlertController
    ) {
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

  repeatVideo() {
    const aux = this.nameSelected;
    this.nameSelected = '';
    setTimeout(() => {
      this.nameSelected = aux;
    }, 100);
  }

  async deleteVideo(name) {
    const alert = await this.alertController.create({
      header: 'Warning',
      message: 'Are you sure to delete this rec?',
      buttons: [
        {
          text: 'Cancel',
          role: 'cancel',
          cssClass: 'secondary'
        }, {
          text: 'Okay',
          handler: () => {
            this.req.deleteVideo(name)
            .subscribe(data => {
              this.updateData();
             }, error => {
              console.log(error);
            });
          }
        }
      ]
    });

    await alert.present();
  }


}
