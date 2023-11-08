import InsertEvent from './InsertEvent';
import InsertParticipant from './InsertParticipant';
import DynamicTable from './Dynamictable';
import React, { useState } from 'react';

// for testing initial connection w/ APIGW
import axios from 'axios';


export default function Home() {
    const [showTable, setShowTable] = useState(false);

    const toggleTableVisibility = () => {
        setShowTable((prevShowTable) => !prevShowTable);
    };

    return (
        <div>
            <h1 style={{marginTop: '4%'}}>Rocking Bussin Microservices Architecture :)</h1>
            <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-around', padding: '3rem'}}>
                {/* Forms directly in the home page for now... maybe tabs or open on button click ? */}
                <InsertEvent />
                <InsertParticipant/> 
            </div>
            <button className = "viewEvents" onClick={toggleTableVisibility}>
                {showTable ? 'Hide Tables' : 'View Tables'}
            </button>
            {showTable && <DynamicTable />}
            
        </div>
    );
}

