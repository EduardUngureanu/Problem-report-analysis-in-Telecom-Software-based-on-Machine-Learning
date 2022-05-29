import * as React from 'react'
import { useState } from 'react'

export function Form(){
    const [pronto, setPronto] = useState("");
    return(
        <form method="POST">
            <label  class="text-3xl font-serif">Prontos details:</label><br />
            <input type="text" name="name" class="appearance-none w-4/6 ll bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4  mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="title" placeholder="Title"/>
            <br />
            <input type="text" name="name" class="appearance-none w-4/6 ll bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4  mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="build" placeholder="Build"/>
            <br />
            <input type="text" name="name" class="appearance-none w-4/6 ll bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4  mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="feature" placeholder="Feature"/>
            <br />
            <input type="text" name="name" class="appearance-none w-4/6 ll bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4  mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="reliase" placeholder="Reliase"/>
            <br />
            <textarea value={pronto} onChange={(e)=>setPronto (e.target.value)} class="appearance-none w-4/6 ll bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4  mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="description" placeholder="Description" />
            <br />
            <button type='submit' name="Btn" value="prediction" class="bg-transparent hover:bg-[#090F30] text-blue-700 font-semibold hover:text-white py-2 px-4 border w-1/3 h-2/6 border-blue-500 hover:border-transparent rounded">Predict</button>
        </form>
    )
}