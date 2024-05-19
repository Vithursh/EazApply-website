import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { Link } from 'react-router-dom';
import '../styles/PremiumPage.css'

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

export const BasicPlan = () => {
    return (
        <div className="bg-dark text-white min-vh-100 d-flex align-items-center min-height">
            <Card className="w-[350px] h-[350px] custom-card">
                <CardHeader>
                <CardTitle className='title'>Basic Plan</CardTitle>
                <CardDescription className='description-heading'>Free</CardDescription>
                <CardDescription className='pricing'>CA$0.00 / month</CardDescription>
                </CardHeader>
                <CardContent>
                <form>
                    <div className="grid w-full items-center gap-4">
                    <div className="flex flex-col space-y-1.5">
                        <Label htmlFor="name" className='feature-list'>Features Included:</Label>
                        <ul className='feature-list'>
                            <li>Apply to 2 jobs a day</li>
                        </ul>
                    </div>
                    </div>
                    <div className='basic-button-position'>
                        <Button className='button-size'>Get Started</Button>
                    </div>
                </form>
                </CardContent>
            </Card>
            {/* <div className="header">
                <h1>Header</h1>
                <p>My supercool header</p>
            </div> */}
        </div>
    );
};

export const StandardPlan = () => {
    return (
        
            <Card className="w-[350px] h-[350px] standard-card">
                <CardHeader>
                <CardTitle className='standard-title'>Standard Plan</CardTitle>
                <CardDescription className='description-heading'>Premium</CardDescription>
                <CardDescription className='pricing'>CA$100.00 / month</CardDescription>
                </CardHeader>
                <CardContent>
                <form>
                    <div className="grid w-full items-center gap-4">
                    <div className="flex flex-col space-y-1.5">
                        <Label htmlFor="name" className='feature-list'>Features Included: </Label>
                        <ul className='feature-list'>
                            <li>Apply to 10 jobs a day</li>
                        </ul>
                    </div>
                    </div>
                    <div className='standard-button-position'>
                        <Button className='button-size'>Get Started</Button>
                    </div>
                </form>
                </CardContent>
            </Card>
        
    );
};

export const ElitePlan = () => {
    return (
        
            <Card className="w-[350px] h-[350px] elite-card">
                <CardHeader>
                <CardTitle className='elite-title'>Elite Plan</CardTitle>
                <CardDescription className='description-heading'>Premium</CardDescription>
                <CardDescription className='pricing'>CA$500.00 / month</CardDescription>
                </CardHeader>
                <CardContent>
                <form>
                    <div className="grid w-full items-center gap-4">
                    <div className="flex flex-col space-y-1.5">
                        <Label htmlFor="name" className='feature-list'>Features Included: </Label>
                        <ul className='feature-list'>
                            <li>Apply to 20 jobs a day</li>
                        </ul>
                    </div>
                    </div>
                    <div className='elite-button-position'>
                        <Button className='button-size'>Get Started</Button>
                    </div>
                </form>
                </CardContent>
            </Card>
    );
};