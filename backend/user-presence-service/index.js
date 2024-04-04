// import React, { useState, useEffect } from "react";
// import BackgroundService from "react-native-background-actions";

// const options = {
//   taskName: "Demo",
//   taskTitle: "Demo Running",
//   taskDesc: "Demo",
//   taskIcon: {
//     name: "ic_launcher",
//     type: "mipmap",
//   },
//   color: "#ff00ff",
//   parameters: {
//     delay: 5000,
//   },
//   actions: '["Exit"]',
// };

// const backgroundTask = async (taskData) => {
//   try {
//   } catch (error) {
//   } finally {
//   }
// };

// const HomeScreen = ({ route, navigation }) => {
//   useEffect(() => {
//     return () => {};
//   }, []);

//   return <div></div>;
// };

// export default HomeScreen;

// import { useEffect } from 'react';
// import { Platform } from 'react-native';
// import BackgroundService from 'react-native-background-actions';

// const MyBackgroundTask = async () => {
//   console.log('Background task is running...');
// };

// const startBackgroundTask = async () => {
//   try {
//     await BackgroundService.registerTask({
//       taskName: 'MyBackgroundTask',
//       taskTitle: 'My Background Task',
//       taskDesc: 'This is a long-running background task',
//       taskIcon: {
//         name: 'ic_launcher',
//         type: 'mipmap',
//       },
//       color: '#ff00ff',
//       parameters: {},
//     });
//     await BackgroundService.start(MyBackgroundTask);
//     console.log('Background task started successfully');
//   } catch (e) {
//     console.error('Failed to start background task:', e);
//   }
// };

// const App = () => {
//   useEffect(() => {
//     startBackgroundTask();

//     // Stop the background task when the component unmounts
//     return () => {
//       BackgroundService.stop();
//     };
//   }, []);

//   return null;
// };

// export default App;


import React, { useState, useEffect } from 'react';
import { Button } from 'react-native';
import BackgroundService from 'react-native-background-actions';

const MyBackgroundTask = async (taskData) => {
  console.log('Background task started:', taskData); 
  console.log('Background task is running...');

  // Simulate some background work
  await new Promise(resolve => setTimeout(resolve, 5000));

  BackgroundService.updateNotification({taskDesc: 'Background listening...'});
  console.log('Background task completed.');
};

const options = {
  taskName: 'Demo',
  taskTitle: 'Demo Running',
  taskDesc: 'Demo',
  taskIcon: {
    name: 'ic_launcher',
    type: 'mipmap',
  },
  color: '#ff00ff',
  parameters: {},
};

const HomeScreen = () => {
  const [isTaskRunning, setIsTaskRunning] = useState(false);
  const registerBackgroundTask = async () => {
    try {
      console.log('Trying to register background task');
      await BackgroundService.start(MyBackgroundTask, options);
      console.log('Background task registered successfully!');
      setIsTaskRunning(true);
    } catch (e) {
      console.error('Failed to register background task:', e);
    }
  };
  const stopBackgroundTask = async () => { 
    try {
      console.log('Stopping background task');
      await BackgroundService.stop();
      console.log('Background task stopped successfully');
      setIsTaskRunning(false);
    } catch (e) {
      console.error('Failed to stop background task:', e);
    }
  };

  return (
    <> {/* Use a Fragment to allow multiple elements */}
      <Button title="Start" onPress={registerBackgroundTask} disabled={isTaskRunning}/>
      <Button title="Stop" onPress={stopBackgroundTask} disabled={!isTaskRunning} />
    </>
  );
};

export default HomeScreen;


