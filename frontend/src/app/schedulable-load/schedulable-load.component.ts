import { Component } from '@angular/core';
import {SidebarComponent} from "../sidebar/sidebar.component";

@Component({
  selector: 'app-schedulable-load',
  standalone: true,
  imports: [
    SidebarComponent
  ],
  templateUrl: './schedulable-load.component.html',
  styleUrl: './schedulable-load.component.css'
})
export class SchedulableLoadComponent {

}
