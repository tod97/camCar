import { Component, OnInit } from '@angular/core';
import { HttpRequestsService } from '../http-requests.service';

@Component({
  selector: 'app-controller',
  templateUrl: './controller.component.html',
  styleUrls: ['./controller.component.scss'],
})
export class ControllerComponent implements OnInit {

  constructor(private req: HttpRequestsService) { }

  ngOnInit() {}

  onTap(position: string) {
    console.log('LOG: Short moving ' + position + '...');
    this.req.socketSend('shortMove', {position});
  }

  onPress(position: string) {
    console.log('LOG: Start moving ' + position + '...');
    this.req.socketSend('startMove', {position});
  }

  onPressUp(position: string) {
    console.log('LOG: Stop moving ' + position + '...');
    this.req.socketSend('stopMove', {});
  }

  /*
  
  /*
  onPress($event, position: string) {
    this.pressState = 'pressing';
    this.movement = position;
    console.log('LOG: Start moving ' + position + '...');
    this.req.move(position);
    this.startInterval();
  }

  onPressUp($event) {
    this.pressState = 'released';
    this.stopInterval();
  }

  startInterval() {
    const self = this;
    this.interval = setInterval(() => {
        console.log('LOG: Moving ' + self.movement + '...');
        this.req.move(self.movement);
    }, 500);
  }

  stopInterval() {
    clearInterval(this.interval);
  }
  */

}
