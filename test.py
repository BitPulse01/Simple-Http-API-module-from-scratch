import main

minimal_info = {
    "price":5050,
    "time":"now",
}

full_data = {
    "price":5050,
    "Lowest_price":5040,
    "Highest_price":5060,
    "time":"now",
}

server = main.API(["/full", "/minimal_data"], {
    "/full":full_data,
    "/minimal_data":minimal_info,
})
