import { configureStore } from '@reduxjs/toolkit';
import enrollmentReducer from './features/enrollmentSlice';
import coursesReducer from './features/coursesSlice';

export const store = configureStore({
  reducer: {
    enrollment: enrollmentReducer,
    courses: coursesReducer
  }
});