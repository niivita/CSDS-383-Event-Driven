import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DynamicTable = () => {
  const [eventData, setEventData] = useState({});
  const [participantData, setParticipantData] = useState({});

  // on load, fetch from DB TODO: APIGW
  useEffect(() => {

    // get dynamoDB contents of event table
    axios.get(`https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/events/`, {}
    ).then(function (response) {
      // handle success
    //   console.log(response);
      setEventData(response.data);

    })
      .catch(function (error) {
        // handle error
        console.log(error);
      })

    // get dynamoDB contents of participants table
    axios.get(`https://t6r6u8jln4.execute-api.us-east-1.amazonaws.com/main/participants/`, {}
    ).then(function (response) {
      // handle success
    //   console.log(response);
      setParticipantData(response.data);

    })
      .catch(function (error) {
        // handle error
        console.log(error);
      })

  }, []);

  // to properly update eventData
  useEffect(() => {
    console.log("eventData updated:", eventData);
  }, [eventData]);

  // to properly update participantData
  useEffect(() => {
    console.log("participantData updated:", participantData);
  }, [participantData]);

  return (
    <div>
      <div className="container1">
        <table>
          <thead>
            <tr>
              <th>UUID</th>
              <th>Date</th>
              <th>Time</th>
              <th>Title</th>
              <th>Description</th>
              <th>Host Email</th>
            </tr>
          </thead>
          <tbody>
            {Object.keys(eventData).length === 0 ? (
              <tr>
                <td colSpan="6">No Events Added Yet!</td>
              </tr>
            ) : (
              Object.keys(eventData).map((index) => {
                return (
                  <tr key={index}>
                    <td>{eventData[index].EventID}</td>
                    <td>{eventData[index].Date}</td>
                    <td>{eventData[index].Time}</td>
                    <td>{eventData[index].Title}</td>
                    <td>{eventData[index].Description}</td>
                    <td>{eventData[index].Email}</td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>
      <div className="container2">
        <table>
          <thead>
            <tr>
              <th>Event ID</th>
              <th>Participant ID</th>
              <th>Name</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {Object.keys(participantData).length === 0 ? (
              <tr>
                <td colSpan="6">No Participants Added Yet!</td>
              </tr>
            ) : (
              Object.keys(participantData).map((index) => {
                return (
                  <tr key={index}>
                    <td>{participantData[index].event_uuid}</td>
                    <td>{participantData[index].participant_uuid}</td>
                    <td>{participantData[index].name}</td>
                    <td>{participantData[index].participant_email}</td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DynamicTable;