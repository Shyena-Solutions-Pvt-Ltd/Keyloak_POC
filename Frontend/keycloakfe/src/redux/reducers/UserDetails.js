import { createSlice } from '@reduxjs/toolkit';

const initialStateValue = {
  userRoles:[]
};

export const userSlice = createSlice({
  name: 'UserDetails',
  initialState: initialStateValue,
  reducers: {
    setUserRoles: (state, action) => {
      state.userRoles = action.payload;
    },
  }
});

export const { setUserRoles } = userSlice.actions;

export default userSlice.reducer;