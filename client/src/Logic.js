 
 import axios from 'axios';
 export async function containsWordsIgnoreCase(text) {
//     const wordsToCheck = ["Suicide", "Kill myself",
//         "End my life","I want to die","Can't go on","Life is pointless","No way out"];
//     let suiciedParam = 0;
//     let numOfSuicideHard = 0;
//     wordsToCheck.map((word, index) => {
//         if(new RegExp(`\\b${word}\\b`, "i").test(text)) {
//             numOfSuicideHard = numOfSuicideHard + 1;
//         }
//     });
//     if (numOfSuicideHard >= 2) {
//         suiciedParam=90;
//     }
//     return suiciedParam;



try {
    const response = await axios.post('http://127.0.0.1:5000/default/calculateSuicidePost', {
      text: text,
    });
    // הנחה שהתשובה מהשרת היא מספר (אם התשובה היא אחרת, יש לעדכן את הפונקציה בהתאם)
    return response.data.suicide_rate; // אם התשובה היא number, תחזור בתור number
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // throwing the error so you can handle it where you call the function
  }


}

