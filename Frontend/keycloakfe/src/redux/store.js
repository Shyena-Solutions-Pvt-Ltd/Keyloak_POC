import { persistReducer } from 'redux-persist';

import storage from 'redux-persist/lib/storage';

import {configureStore} from '@reduxjs/toolkit';

import { combineReducers } from 'redux';

import UserReducer from './reducers/UserDetails'


const persistConfig = {
    key: 'root',
    storage,
};

const reducers = combineReducers({
    UserDetails : UserReducer,
})

const persistedReducer = persistReducer(persistConfig, reducers);

const store = configureStore({
    reducer: persistedReducer,
    middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

export default store;