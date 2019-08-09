import { Component } from '@angular/core';

import { HttpRequestsService } from '../http-requests.service';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {

  controller: any;
  controllerData: any;

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
    this.controller.on('move', (evt, data) => {
      switch (evt.type) {
        case 'move':
          this.req.socketSend('move', this.calculatePower(data.distance, data.direction.x, data.direction.y, data.angle.radian));
          break;
      }
    });
  }

  calculatePower(distance: number, x: string, y: string, radian: number) {
    let dLeft: number, dRight: number;
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

  connect() {
    this.req.socketConnect();
  }

  disconnect() {
    this.req.socketDisconnect();
  }
}
