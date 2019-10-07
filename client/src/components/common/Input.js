import React from 'react'

const Input = (props) => {


    return (
        <div className="TextInput form-group">
            <label for="exampleInputEmail1">{props.label}</label>
            {props.name === "start" || props.name === "end" ? (
                <input
                    type={props.type}
                    name={props.name}
                    value={props.value}
                    onChange={props.onChange}
                    onBlur={props.onBlur}
                    className="form-control"
                    aria-describedby="emailHelp"
                    placeholder={props.placeholder}
                    required />
            ) : (
                    <input
                        type={props.type}
                        name={props.name}
                        value={props.value}
                        onChange={props.onChange}
                        className="form-control"
                        aria-describedby="emailHelp"
                        placeholder={props.placeholder}
                        required />


                )}
            {props.radioMessage}
            <small id="emailHelp" className="form-text text-muted"> {props.message}</small>
            <small id="emailHelp" className="form-text text-muted"> {props.error}</small>
        </div>
    )
}

export default Input;