import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CourseCard } from '../course-card/course-card';
import { Course } from '../course';

@Component({
  selector: 'app-course-list',
  imports: [CommonModule, FormsModule, CourseCard],
  templateUrl: './course-list.html',
  styleUrl: './course-list.css'
})
export class CourseList implements OnInit {
  searchTerm = '';
  courses: any[] = [];
  loading = true;

  constructor(private courseService: Course) {}

  ngOnInit() {
    this.loading = true;
    this.courseService.getCourses().subscribe((posts: any[]) => {
      this.courses = posts.map((post, index) => ({
        id: post.id,
        name: post.title,
        code: 'CS10' + (index + 1),
        credits: 3,
        grade: 'A'
      }));
      this.loading = false;
    });
  }

  get filteredCourses() {
    return this.courses.filter(course =>
      course.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }
}