import * as React from 'react'
import {Form} from '../../components/Form'
import {Output} from '../../components/Output'

export function Home(){
    return(
        <>
        <div class="py-5 text-6xl font-serif bg-[#090F30] text-white"> Predict page for prontos </div>
        <hr class="leading-8" />
        <br />
        <Form/>
        <Output/>
        </>
    )
}

