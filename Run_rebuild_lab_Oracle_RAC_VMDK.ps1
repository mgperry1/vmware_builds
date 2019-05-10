## ScriptTest.ps1
# Mandatory Switches; Master1; DataStore; vcuser; vcpass


function OracleRacDisks {
    param (
        [Parameter()]
        [ValidateNotNullOrEmpty()]
        [string]$Master1,
    
        [Parameter()]
        [string]
        $Master2,
        
        [Parameter()]
        [string]
        $Master3,
    
        [Parameter()]
        [string]
        $DataStore,
    
        [Parameter()]
        [string]
        $vcname,
    
        [Parameter()]
        [ValidateNotNullOrEmpty()]
        [string]$vcuser,
    
        [Parameter()]
        [ValidateNotNullOrEmpty()]
        [string]
        $vcpass
    )
    
    if (!$IsLinux) {
        Write-Warning -Message "Exiting; not a linux computer."
    }
    #Write-Host "Path:" $PSScriptRoot

    $ScriptName = '/rebuild_lab_Oracle_RAC_VMDK.ps1'
    $RebuildLAB_RACs = $PSScriptRoot + $ScriptName
    Write-Host $RebuildLAB_RACs
    # These if blocks below can be changed to static variables 
    # if you would rather not pass them into the script at runtime.
    if (!$vcname) {
        $vcname = "vc-irv.techlab.com"
    }
    # if (!$vcuser) {
    #     # Put your vcenter username here
    #     $vcuser = $null
    # }
    # if (!$vcpass) {
    #     # Put your vcenter password here
    #     $vcpass = $null
    # }
    # if (!$Master1) {
    #     # This is the name of the VM that is the master node of an Oracle RAC
    #     $Master1 = $null
    # }
    # if (!$Master2) {
    #     $Master2 = $null
    # }
    # if (!$Master3) {
    #     $Master3 = $null
    # }
    # if (!$DataStore) {
    #     # Name of the datastore to create VMDKs in.
    #     # for example: '[pure_vmfs6_03]'
    #     $Datastore = $null
    # }

    # If Master[1/2/3] variables are set, then the script will run and target the Master Node by VM Name
    if (Get-Variable -Name Master1 -ErrorAction SilentlyContinue) {
        Write-Host "Running Script against Master1..."
        & $RebuildLAB_RACs -MasterNode $Master1 -DataStore $Datastore -vcname $vcname -vcuser $vcuser -vcpass $vcpass
    }
    if ($Master2) {
        & $RebuildLAB_RACs -MasterNode $Master2 -DataStore $Datastore -vcname $vcname -vcuser $vcuser -vcpass $vcpass
    }
    if ($Master3) {
        & $RebuildLAB_RACs -MasterNode $Master3 -DataStore $Datastore -vcname $vcname -vcuser $vcuser -vcpass $vcpass
    }

}

OracleRacDisks