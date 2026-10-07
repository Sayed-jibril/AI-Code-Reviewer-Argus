' VB.NET test file with various issues
Imports System.Data.SqlClient

Public Class BadClass
    
    Private apiKey As String = "sk-1234567890abcdef" ' Hardcoded secret
    
    Public Sub BadFunction(userInput As String)
        ' SQL concatenation; use parameters
        Dim query As String = "SELECT * FROM users WHERE id = " & userInput
        Dim cmd As New SqlCommand(query)
        
        ' MD5 is weak; prefer SHA256
        Dim md5 As System.Security.Cryptography.MD5 = System.Security.Cryptography.MD5.Create()
        
        ' On Error Resume Next hides failures
        On Error Resume Next
        
        ' Empty catch block
        Try
            ' Some operation
        Catch ex As Exception
            ' Empty catch block
        End Try
        
        ' Nested loops
        For i As Integer = 0 To 9
            For j As Integer = 0 To 9
                For k As Integer = 0 To 9
                    Console.WriteLine(i & ", " & j & ", " & k)
                Next
            Next
        Next
    End Sub
    
    Public Function AnotherFunction() As String
        ' Function definition
        Return "result"
    End Function
End Class
