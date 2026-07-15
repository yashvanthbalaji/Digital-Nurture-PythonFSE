import { createSlice } from '@reduxjs/toolkit';

const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState: { enrolledCourses: [] },
  reducers: {
    enroll: (state, action) => {
      state.enrolledCourses.push(action.payload);
    },
    unenroll: (state, action) => {
      state.enrolledCourses = state.enrolledCourses.filter(
        course => course.id !== action.payload
      );
    }
  }
});

export const { enroll, unenroll } = enrollmentSlice.actions;
export default enrollmentSlice.reducer;