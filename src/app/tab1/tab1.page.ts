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

  setCamera(update = false) {
    this.connect();
    if (update) {
      this.showCamera = !this.showCamera;
    }
    if (this.showCamera) {
      setTimeout(() => {
        this.req.socketSend('video', {});
        if (this.req.socketConnect && this.showCamera) {
          this.setCamera();
        }
      }, 1000);
    } else {
      this.req.frame = '';
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

  turn(angle) {
    this.req.socketSend('turn', {angle});
  }

  connect() {
    this.req.socketConnect();
  }

  disconnect() {
    this.showCamera = false;
    this.req.socketDisconnect();
  }
}
