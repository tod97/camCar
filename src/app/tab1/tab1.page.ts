import { Component } from '@angular/core';

import { HttpRequestsService } from '../http-requests.service';

declare var require: any;

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {

  controller: any;
  controllerData: any;
  showCamera = false;
  isRecording = false;

  constructor(private req: HttpRequestsService) {
  }

  ionViewDidEnter() {
    this.controller = require('nipplejs').create({
      color: 'black',
      mode: 'static',
      position: {left: '50%', top: '50%'},
      size: 200,
      zone: document.getElementById('zone_joystick')
    });
    this.controller.on('move end', (evt, data) => {
      switch (evt.type) {
        case 'move':
          if (data.direction) {
            this.req.socketSend('move', this.calculatePower(data.distance, data.direction.x, data.direction.y, data.angle.radian));
          }
          break;
        case 'end':
          this.req.socketSend('stopMove', {});
          break;
      }
    });
  }

  setCamera() {
    if (this.showCamera) {
      this.showCamera = false;
    } else {
      if (this.req.socketConnected) {
        this.showCamera = true;
      } else {
        this.connect();
      }
    }
  }

  calculatePower(distance: number, x: string, y: string, radian: number) {
    let dLeft, dRight;
    if (x === 'right' && y === 'up') {
      dLeft = distance;
      dRight = distance * Math.sin(radian);
    }
    if (x === 'left' && y === 'up') {
      dLeft = distance * Math.sin(radian);
      dRight = distance;
    }
    if (x === 'left' && y === 'down') {
      dLeft = distance * Math.sin(radian);
      dRight = -distance;
    }
    if (x === 'right' && y === 'down') {
      dLeft = -distance;
      dRight = distance * Math.sin(radian);
    }
    return {dLeft, dRight};
  }

  recordStart() {
    this.req.recordVideo(true)
    .subscribe(data => {
      this.isRecording = true;
     }, error => {
      console.log(error);
    });
  }

  recordStop() {
    this.req.recordVideo(false)
    .subscribe(data => {
      this.isRecording = false;
     }, error => {
      console.log(error);
    });
  }

  connect() {
    this.req.socketConnect();
  }

  disconnect() {
    this.showCamera = false;
    this.req.socketDisconnect();
  }
}
